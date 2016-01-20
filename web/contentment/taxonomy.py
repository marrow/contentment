# encoding: utf-8

from itertools import chain
from operator import __or__
from functools import reduce
from bson import ObjectId, DBRef, SON
from mongoengine import QuerySet, Q
from mongoengine import Document, ListField, StringField, IntField, ObjectIdField
from mongoengine import ReferenceField
from mongoengine.signals import pre_delete
from mongoengine.common import _import_class
from mongoengine.base.fields import ComplexBaseField
from mongoengine.base.datastructures import EmbeddedDocumentList, BaseList, BaseDict
from mongoengine import EmbeddedDocument
from mongoengine.dereference import DeReference
from mongoengine.base import get_document, TopLevelDocumentMetaclass

from .util.model import signal

log = __import__('logging').getLogger(__name__)


@signal(pre_delete)
def remove_children(sender, document, **kw):
	document.empty()


class CustomDereference(DeReference):
	def _find_references(self, items, depth=0, finded_ids=None):
		"""
		Recursively finds all db references to be dereferenced

		:param items: The iterable (dict, list, queryset)
		:param depth: The current depth of recursion
		"""
		# if items and isinstance(items, list) and getattr(items[0], 'name', '') == 'child2':
		# 	import pudb; pudb.set_trace()
		reference_map = {}
		if not items or depth >= self.max_depth:
			return reference_map

		# Determine the iterator to use
		if not hasattr(items, 'items'):
			iterator = enumerate(items)
		else:
			iterator = iter(items.items())

		# Recursively find dbreferences
		depth += 1
		processed_ids = finded_ids if finded_ids is not None else set()
		for k, item in iterator:
			if isinstance(item, (Document, EmbeddedDocument)):
				for field_name, field in item._fields.items():
					v = item._data.get(field_name, None)
					if (v and getattr(field, 'document_type', object) is Taxonomy and
							isinstance(v, Taxonomy) and
							v.id not in processed_ids):
						processed_ids.add(v.id)
						reference_map.setdefault(type(v), set()).add(v.id)
					elif isinstance(v, DBRef) and v.id not in processed_ids:
						processed_ids.add(v.id)
						try:
							reference_map.setdefault(get_document(v.cls), set()).add(v.id)
						except AttributeError:
							reference_map.setdefault(field.document_type, set()).add(v.id)
					elif isinstance(v, (dict, SON)) and '_ref' in v and v['_ref'].id not in processed_ids:
						processed_ids.add(v['_ref'].id)
						reference_map.setdefault(get_document(v['_cls']), set()).add(v['_ref'].id)
					elif isinstance(v, (dict, list, tuple)) and depth <= self.max_depth:
						field_cls = getattr(getattr(field, 'field', None), 'document_type', None)
						references = self._find_references(v, depth, processed_ids)
						for key, refs in references.items():
							if isinstance(field_cls, (Document, TopLevelDocumentMetaclass)) and key is Taxonomy:
								key = field_cls
							reference_map.setdefault(key, set()).update(refs)
			elif isinstance(item, DBRef) and item.id not in processed_ids:
				processed_ids.add(item.id)
				reference_map.setdefault(item.collection, set()).add(item.id)
			elif isinstance(item, (dict, SON)) and '_ref' in item and item['_ref'].id not in processed_ids:
				processed_ids.add(item['_ref'].id)
				reference_map.setdefault(get_document(item['_cls']), set()).add(item['_ref'].id)
			elif isinstance(item, (dict, list, tuple)) and depth - 1 <= self.max_depth:
				references = self._find_references(item, depth - 1, processed_ids)
				for key, refs in references.items():
					reference_map.setdefault(key, set()).update(refs)

		return reference_map


class TaxonomyQuerySet(QuerySet):
	def __init__(self, document, collection, _rewrite_initial=False):
		super(TaxonomyQuerySet, self).__init__(document, collection)
		self.__dereference = None
		if _rewrite_initial:
			self._initial_query = {'_cls': {'$in': Taxonomy._subclasses}}

	@property
	def _dereference(self):
		if not self.__dereference:
			self.__dereference = CustomDereference()
		return self.__dereference

	@property
	def base_query(self):
		return TaxonomyQuerySet(Taxonomy, self._collection)

	# Quick Lookup

	def named(self, name):
		return self.filter(name=name)

	def nearest(self, path):
		if hasattr(path, 'split'):
			path = path.split('/')

		# Remove leading empty elements.
		while path and not path[0]:
			del path[0]

		# Remove trailing empty elements.
		while path and not path[-1]:
			del path[-1]

		# Determine the full list of possible paths.
		paths = [('/' + '/'.join(path[:i])) for i in range(len(path) + 1)]

		log.debug("Searching for element nearest: /" + '/'.join(path), extra=dict(search=paths))

		# Find the deepest (completely or partially) matching asset.
		return self.clone().filter(path__in=paths).order_by('-path').first()

	# Basic Management

	def empty(self, *q_objs, **query):
		"""Delete all descendants of the currently selected assets.

		Warning: If run on all assets this will only leave the root element intact. It would also be expensive.
		"""

		# import ipdb; ipdb.set_trace()

		parents = self.clone().filter(*q_objs, **query)

		# Optimization note: this doesn't need to worry about normalizing paths, thus the _from_doc_delete.
		# TODO: Handle potential exception: signal handlers may preemptively delete included records. That's perfectly ok!
		self.base_query(parents__in=parents).delete(write_concern=None, _from_doc_delete=True)  # TODO: write_concern

		# Returns original QuerySet, as it'll need to re-query to check if any included results survive.
		return self
	
	def insert(self, index, child):
		"""Add an asset, specified by the parameter, as a child of this asset."""
		
		parent = self.clone().first()
		
		log.info("Inserting asset.", extra=dict(asset=parent.id, index=index, child=getattr(child, 'id', child)))
		
		# Detach the new child (and thus it's own child nodes).
		child = (self.base_query.get(id=child) if isinstance(child, ObjectId) else child).detach(False)
		
		if index < 0:
			_max = self.base_query(parent=parent).order_by('-order').scalar('order').first()
			index = 0 if _max is None else (_max + 1)
		
		q = self.base_query(parent=parent, order__gte=index).update(inc__order=1)
		
		child.order = index
		
		child.path = parent.path + '/' + child.name
		child.parent = parent
		child.parents = list(parent.parents)
		child.parents.append(parent)
		
		child = child.save()
		
		child.contents.update(__raw__={
				'$push': {
						child.db_field_map['parents']: {
								'$each': [
										i.to_dbref() for i in child.parents
									],
								'$position': 0
							}
					}
			})
		
		child._normpath()
		
		return self
	
	def detach(self, path=True):
		"""Detach this asset from its current taxonomy."""
		
		obj = self.clone().first()
		
		if obj.path in (None, '', obj.name):
			return obj
		
		log.warn("Detaching from taxonomy.", extra=dict(asset=repr(obj), path=path))
		
		self.nextAll.update(inc__order=-1)
		self.contents.update(pull_all__parents=obj.parents)
		
		obj.order = None
		obj.path = obj.name
		obj.parent = None
		obj.parents.clear()  # We can't use `del obj.parents[:]` because MongoEngine detects that.
		obj.save()
		
		if path:
			obj._normpath()
		
		return obj
	
	def append(self, child):
		"""Insert an asset, specified by the parameter, as a child of this asset."""
		return self.insert(-1, child)
	
	def prepend(self, child):
		return self.insert(0, child)
	
	def after(self, sibling):
		"""Insert an asset, specified by the parameter, after this asset."""
		obj = self.clone().first()
		obj.parent.insert(obj.order + 1, sibling)
		return self
	
	def before(self, sibling):
		"""Insert an asset, specified by the parameter, before this asset."""
		obj = self.clone().first()
		obj.parent.insert(obj.order, sibling)
		return self
	
	def replace(self, target):
		"""Replace an asset, specified by the parameter, with this asset."""
		
		target = self.clone().get(id=target) if isinstance(target, ObjectId) else target
		obj = self.clone().first()
		
		obj.name = target.name
		obj.parent = target.parent
		obj.parents = target.parents
		obj.path = target.path
		obj.order = target.order
		
		target.delete()
		obj.save()
		
		return self
	
	def replaceWith(self, source):
		"""Replace this asset with an asset specified by the parameter."""
		
		source = self.clone().get(id=source) if isinstance(source, ObjectId) else source
		obj = self.clone().first()
		
		source.name = obj.name
		source.parent = obj.parent
		source.parents = obj.parents
		source.path = obj.path
		source.order = obj.order
		
		obj.delete()
		source.save()
		
		return self

	def clone_assets(self):
		clones = self.clone()
		for clone in clones:
			del clone.id
		
		return clones
	
	# Pivoted Manipulation
	# These are actually implemented elsewhere.
	
	def appendTo(self, parent):
		"""Insert this asset as a child of the asset specified by the parameter."""
		return self.base_query(pk=getattr(parent, 'pk', parent)).append(self.clone().first())
	
	def prependTo(self, parent):
		"""Insert this asset as the left-most child of the asset specified by the parameter."""
		return self.base_query(pk=getattr(parent, 'pk', parent)).prepend(self.clone().first())
	
	def insertBefore(self, sibling):
		"""Insert this asset as the left-hand sibling of the asset specified by the parameter."""
		return self.base_query(pk=getattr(sibling, 'pk', sibling)).before(self.clone().first())
	
	def insertAfter(self, sibling):
		"""Insert this asset as the right-hand child of the asset specified by the parameter."""
		return self.base_query(pk=getattr(sibling, 'pk', sibling)).after(self.clone().first())
	
	# Traversal
	
	@property
	def children(self):
		"""Yield all direct children of this asset."""
		return self.base_query(parent__in=self.clone())
	
	@property
	def contents(self):
		"""Yield all descendants of this asset."""
		return self.base_query(parents__in=self.clone())
	
	@property
	def siblings(self):
		"""All siblings of the currently selected assets, not including these assets."""
		
		query = []
		
		for id, parent in self.clone().scalar('id', 'parent'):#.no_dereference():
			query.append(Q(parent=parent, id__ne=id))
		
		if not query:  # TODO: Armour everywhere.
			return None
		
		return self.base_query(reduce(__or__, query)).order_by('parent', 'order')
	
	@property
	def next(self):
		"""The sibling immediately following this asset."""
		from operator import __or__
		from functools import reduce
		
		query = []
		
		for parent, order in self.clone().scalar('parent', 'order'):#.no_dereference():
			query.append(Q(parent=parent, order=order + 1))
		
		if not query:
			return None
		
		return self.base_query(reduce(__or__, query)).order_by('path').first()

	@property
	def nextAll(self):
		"""All siblings following this asset."""
		from operator import __or__
		from functools import reduce

		query = []

		# Indexing note: (parent, order, id) for covered query and optimal re-use.
		# Including id here to prevent an edge case (assets being shuffled) from including non-siblings.
		for id, parent, order in self.clone().scalar('id', 'parent', 'order'):#.no_dereference():
			query.append(Q(parent=parent, order__gt=order, id__ne=id))

		if not query:
			return None

		return self.base_query(reduce(__or__, query)).order_by('parent', 'order')

	@property
	def prev(self):
		"""The sibling immediately preceeding this asset."""
		from operator import __or__
		from functools import reduce

		query = []

		for parent, order in self.clone().scalar('parent', 'order'):#.no_dereference():
			query.append(Q(parent=parent, order=order - 1))

		if not query:
			return None

		return self.base_query(reduce(__or__, query)).order_by('parent').first()

	@property
	def prevAll(self):
		"""All siblings preceeding the selected assets."""

		from operator import __or__
		from functools import reduce

		query = []

		for parent, order in self.clone().scalar('parent', 'order'):#.no_dereference():
			query.append(Q(parent=parent, order__lt=order))

		if not query:
			return None

		return self.base_query(reduce(__or__, query)).order_by('parent', 'order')

	def contains(self, other):
		"""The asset, specified by the parameter, is a descendant of any of the selected assets."""

		if __debug__:  # Can be optimized away (-O) in production.
			from web.component.asset import Asset
			assert isinstance(other, Asset) or isinstance(other, ObjectId), "Argument must be Asset or ObjectId instance."

		parents = self.clone().scalar('id').no_dereference()
		return bool(self.base_query(pk=getattr(other, 'pk', other), parents__in=parents).count())

	def extend(self, *others):
		"""Merge the contents of another asset or assets, specified by positional parameters, with this one."""
		obj = self.clone().first()
		for other in others:
			for child in other.children:
				obj.insert(-1, child)
		return self


class CustomDereferenceMixin(ComplexBaseField):
	def __get__(self, instance, owner):
		"""Descriptor to automatically dereference references.
		"""
		if instance is None:
			# Document class being used rather than a document object
			return self

		ReferenceField = _import_class('ReferenceField')
		GenericReferenceField = _import_class('GenericReferenceField')
		EmbeddedDocumentListField = _import_class('EmbeddedDocumentListField')
		dereference = (self._auto_dereference and
					   (self.field is None or isinstance(self.field,
														 (GenericReferenceField, ReferenceField))))

		_dereference = CustomDereference()

		self._auto_dereference = instance._fields[self.name]._auto_dereference
		if instance._initialised and dereference and instance._data.get(self.name):
			instance._data[self.name] = _dereference(
				instance._data.get(self.name), max_depth=1, instance=instance,
				name=self.name
			)

		value = super(ComplexBaseField, self).__get__(instance, owner)

		# Convert lists / values so we can watch for any changes on them
		if isinstance(value, (list, tuple)):
			if (issubclass(type(self), EmbeddedDocumentListField) and
					not isinstance(value, EmbeddedDocumentList)):
				value = EmbeddedDocumentList(value, instance, self.name)
			elif not isinstance(value, BaseList):
				value = BaseList(value, instance, self.name)
			instance._data[self.name] = value
		elif isinstance(value, dict) and not isinstance(value, BaseDict):
			value = BaseDict(value, instance, self.name)
			instance._data[self.name] = value

		if (self._auto_dereference and instance._initialised and
				isinstance(value, (BaseList, BaseDict)) and
				not value._dereferenced):
			value = _dereference(
				value, max_depth=1, instance=instance, name=self.name
			)
			value._dereferenced = True
			instance._data[self.name] = value

		return value


class CustomListField(CustomDereferenceMixin, ListField):
	pass


class Taxonomy(Document):
	meta = dict(
		id_field = 'id',
		ordering = ['order'],
		allow_inheritance = True,
		abstract = True,
		queryset_class = TaxonomyQuerySet,
	)
	
	parent = ReferenceField(
			'self',
			db_field = 't_p',
			export = False
		)
	parents = CustomListField(ReferenceField(  # Serious quesiton as to why custom?  --A
			'self',
		), db_field='t_a', export=False)
	
	id = ObjectIdField(db_field='_id', primary_key=True, default=ObjectId)
	name = StringField(db_field='n')
	path = StringField(db_field='t_P', unique=True)
	order = IntField(db_field='t_o', default=0)
	
	def __repr__(self):
		return "{0.__class__.__name__} ({0.name}, {0.path})".format(self)
	
	@property
	def _qs(self):
		"""Return the queryset for updating, reloading, and deletions."""
		
		if not hasattr(self, '__objects'):
			self.__objects = self.tqs
		
		return self.__objects
	
	@property
	def tqs(self):
		return TaxonomyQuerySet(self.__class__, self._get_collection(), _rewrite_initial=True)
	
	def tree(self, indent=''):
		"""Visualization of the Asset tree."""
		
		print(indent, repr(self), sep="")

		for child in self.children:
			child.tree(indent + "\t")

	def _normpath(self):
		"""Recalculate the paths for all descendants of this asset."""
		
		cache = {}
		
		descendants = self.contents.order_by('path').no_dereference().only('parent', 'name')
		
		for i, child in enumerate(descendants):
			pid = str(child.parent._id)
			
			if pid not in cache:
				cache[pid] = self.tqs(id=child.parent._id).scalar('path')
			
			parent_path = cache[child.parent._id]
			
			child.update(set__path=parent_path + '/' + child.name)
		
		return i
	
	def empty(self):
		self.tqs(id=self.id).empty()

	def detach(self, path=True):
		"""Detach this asset from its current taxonomy."""
		self.tqs(id=self.id).detach(path)
		return self.reload()

	def insert(self, index, child):
		"""Add an asset, specified by the parameter, as a child of this asset."""
		self.tqs(id=self.id).insert(index, child)
		return self.reload()

	def append(self, child):
		"""Insert an asset, specified by the parameter, as a child of this asset."""
		self.tqs(id=self.id).append(child)
		return self

	def prepend(self, child):
		self.tqs(id=self.id).prepend(child)
		return self

	def after(self, sibling):
		"""Insert an asset, specified by the parameter, after this asset."""
		self.tqs(id=self.id).after(sibling)
		return self

	def before(self, sibling):
		"""Insert an asset, specified by the parameter, before this asset."""
		self.tqs(id=self.id).before(sibling)
		return self

	def replace(self, target):
		"""Replace an asset, specified by the parameter, with this asset."""
		self.tqs(id=self.id).replace(target)
		return self

	def replaceWith(self, source):
		"""Replace this asset with an asset specified by the parameter."""
		self.tqs(id=self.id).replaceWith(source)
		return source

	def clone(self):
		return self.tqs(id=self.id).clone_assets()[0]

	def appendTo(self, parent):
		"""Insert this asset as a child of the asset specified by the parameter."""
		self.tqs(id=self.id).appendTo(parent)
		return self

	def prependTo(self, parent):
		"""Insert this asset as the left-most child of the asset specified by the parameter."""
		self.tqs(id=self.id).prependTo(parent)
		return self

	def insertBefore(self, sibling):
		"""Insert this asset as the left-hand sibling of the asset specified by the parameter."""
		self.tqs(id=self.id).insertBefore(sibling)
		return self

	def insertAfter(self, sibling):
		"""Insert his asset as the right-hand child of the asset specified by the parameter."""
		self.tqs(id=self.id).insertAfter(sibling)
		return self

	@property
	def children(self):
		"""Yield all direct children of this asset."""
		return self.tqs(id=self.id).children

	@property
	def contents(self):
		"""Yield all descendants of this asset."""
		return self.tqs(id=self.id).contents

	@property
	def siblings(self):
		"""All siblings of this asset, not including this asset."""
		return self.tqs(id=self.id).siblings

	@property
	def next(self):
		"""The sibling immediately following this asset."""
		return self.tqs(id=self.id).next

	@property
	def nextAll(self):
		"""All siblings following this asset."""
		return self.tqs(id=self.id).nextAll

	@property
	def prev(self):
		"""The sibling immediately preceeding this asset."""
		return self.tqs(id=self.id).prev

	@property
	def prevAll(self):
		"""All siblings preceeding this asset."""
		return self.tqs(id=self.id).prevAll

	def contains(self, other):
		"""The asset, specified by the parameter, is a descendant of this asset."""
		return self.tqs(id=self.id).contains(other)

	def extend(self, *others):
		"""Merge the contents of another asset or assets, specified by positional parameters, with this one."""
		self.tqs(id=self.id).extend(*others)
		return self
