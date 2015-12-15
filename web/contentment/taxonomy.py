# encoding: utf-8

from itertools import chain

from bson import ObjectId
from mongoengine import QuerySet, Q
from mongoengine import Document, ListField, StringField, IntField
from mongoengine import CachedReferenceField, ReferenceField
from mongoengine.fields import RECURSIVE_REFERENCE_CONSTANT
from mongoengine.signals import pre_delete

from .util.model import signal

log = __import__('logging').getLogger(__name__)


@signal(pre_delete)
def remove_children(sender, document, **kw):
	document.empty()


class TaxonomyQuerySet(QuerySet):
	def __init__(self, document, collection):
		super(TaxonomyQuerySet, self).__init__(document, collection)
		if self._document is Taxonomy:
			self._initial_query = {'_cls': {'$in': Taxonomy._subclasses}}

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

		parents = self.clone().filter(*q_objs, **query).scalar('id')

		# Optimization note: this doesn't need to worry about normalizing paths, thus the _from_doc_delete.
		# TODO: Handle potential exception: signal handlers may preemptively delete included records. That's perfectly ok!
		self._document.objects(parents__in=parents).delete(write_concern=None, _from_doc_delete=True)  # TODO: write_concern

		# Returns original QuerySet, as it'll need to re-query to check if any included results survive.
		return self

	def insert(self, index, child):
		"""Add an asset, specified by the parameter, as a child of this asset."""

		parent = self.clone().first()

		log.info("Inserting asset.", extra=dict(asset=parent.id, index=index, child=getattr(child, 'id', child)))

		# Detach the new child (and thus it's own child nodes).
		child = (self._document.objects.get(id=child) if isinstance(child, ObjectId) else child).detach(False)

		if index < 0:
			_max = self._document.objects(parent=parent).order_by('-order').scalar('order').first()
			index = 0 if _max is None else (_max + 1)

		q = self._document.objects(parent=parent, order__gte=index).update(inc__order=1)

		log.debug("before", extra=dict(data=repr(child._data)))

		child.order = index

		child.path = parent.path + '/' + child.name
		child.parent = parent
		child.parents = list(parent.parents)
		child.parents.append(parent)

		log.debug("after", extra=dict(data=repr(child._data)))

		child = child.save()

		print("Child contents:", child.contents)
		child.contents.update(__raw__={'$push': {'t_a': {'$each': [i.to_dbref() for i in child.parents], '$position': 0}}})
		# child.contents.update(push__ancestors={'$each': ancestors, '$position': 0})  # Unimplemented.

		parent._normpath(child.id)

		return self

	def detach(self, path=True):
		"""Detach this asset from its current taxonomy."""

		obj = self.clone().first()

		if obj.path in (None, '', obj.name):
			return obj

		log.warn("Detaching from taxonomy." + "\n\t" + __import__('json').dumps(dict(asset=repr(obj), path=path)))

		self.nextAll.update(inc__order=-1)

		self.contents.update(parents__pull_all=obj.parents)

		obj.order = None
		obj.path = obj.name
		obj.parent = None
		del obj.parents[:]

		if path:
			obj._normpath(obj.id)

		obj.save()

		return self

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
		return self._document.objects(pk=getattr(parent, 'pk', parent)).append(self.clone().first())

	def prependTo(self, parent):
		"""Insert this asset as the left-most child of the asset specified by the parameter."""
		return self._document.objects(pk=getattr(parent, 'pk', parent)).prepend(self.clone().first())

	def insertBefore(self, sibling):
		"""Insert this asset as the left-hand sibling of the asset specified by the parameter."""
		return self._document.objects(pk=getattr(sibling, 'pk', sibling)).before(self.clone().first())

	def insertAfter(self, sibling):
		"""Insert this asset as the right-hand child of the asset specified by the parameter."""
		return self._document.objects(pk=getattr(sibling, 'pk', sibling)).after(self.clone().first())

	# Traversal

	@property
	def children(self):
		"""Yield all direct children of this asset."""

		return self._document.objects(parent__in=list(self.clone().scalar('id'))).order_by('parent', 'order')

	@property
	def contents(self):
		"""Yield all descendants of this asset."""

		return self._document.objects(parents__in=self.clone().scalar('id').all()).order_by('parent', 'order')

	@property
	def siblings(self):
		"""All siblings of the currently selected assets, not including these assets."""
		from operator import __or__
		from functools import reduce

		query = []

		for id, parent in self.clone().scalar('id', 'parent').no_dereference():
			query.append(Q(parent=parent, id__ne=id))

		if not query:  # TODO: Armour everywhere.
			return None

		return self._document.objects(reduce(__or__, query)).order_by('parent', 'order')

	@property
	def next(self):
		"""The sibling immediately following this asset."""
		from operator import __or__
		from functools import reduce

		query = []

		for parent, order in self.clone().scalar('parent', 'order').no_dereference():
			query.append(Q(parent=parent, order=order + 1))

		if not query:
			return None

		return self._document.objects(reduce(__or__, query)).order_by('path').first()

	@property
	def nextAll(self):
		"""All siblings following this asset."""
		from operator import __or__
		from functools import reduce

		query = []

		# Indexing note: (parent, order, id) for covered query and optimal re-use.
		# Including id here to prevent an edge case (assets being shuffled) from including non-siblings.
		for id, parent, order in self.clone().scalar('id', 'parent', 'order').no_dereference():
			query.append(Q(parent=parent, order__gt=order, id__ne=id))

		if not query:
			return None

		return self._document.objects(reduce(__or__, query)).order_by('parent', 'order')

	@property
	def prev(self):
		"""The sibling immediately preceeding this asset."""
		from operator import __or__
		from functools import reduce

		query = []

		for parent, order in self.clone().scalar('parent', 'order').no_dereference():
			query.append(Q(parent=parent, order=order - 1))

		if not query:
			return None

		return self._document.objects(reduce(__or__, query)).order_by('parent').first()

	@property
	def prevAll(self):
		"""All siblings preceeding the selected assets."""

		from operator import __or__
		from functools import reduce

		query = []

		for parent, order in self.clone().scalar('parent', 'order').no_dereference():
			query.append(Q(parent=parent, order__lt=order))

		if not query:
			return None

		return self._document.objects(reduce(__or__, query)).order_by('parent', 'order')

	def contains(self, other):
		"""The asset, specified by the parameter, is a descendant of any of the selected assets."""

		if __debug__:  # Can be optimized away (-O) in production.
			from web.component.asset import Asset
			assert isinstance(other, Asset) or isinstance(other, ObjectId), "Argument must be Asset or ObjectId instance."

		parents = self.clone().scalar('id').no_dereference()
		return bool(self._document.objects(pk=getattr(other, 'pk', other), parents__in=parents).count())

	def extend(self, *others):
		"""Merge the contents of another asset or assets, specified by positional parameters, with this one."""
		obj = self.clone().first()
		for other in others:
			for child in other.children:
				obj.insert(-1, child)
		return self


class Taxonomy(Document):
	meta = dict(
		# id_field = 'id',
		ordering = ['order'],
		allow_inheritance = True,
		# abstract = True,
		queryset_class = TaxonomyQuerySet,
	)

	# parent = CachedReferenceField(
	parent = ReferenceField(
			'self',
			db_field = 't_p',
			# fields = ['name'],
			export=False
		)
	# parents = ListField(CachedReferenceField(
	parents = ListField(ReferenceField(
			'self',
			# fields = ['name', 'acl'],
		), db_field='t_a', export=False)

	name = StringField(db_field='n', export=True, simple=True)
	path = StringField(db_field='t_P', unique=True, export=True, simple=True)
	order = IntField(db_field='t_o', default=0, export=True, simple=True)

	def __repr__(self):
		return "{0.__class__.__name__} ({0.name}, {0.path})".format(self)
	
	@property
	def tqs(self):
		return TaxonomyQuerySet(Taxonomy, self._get_collection())

	def tree(self, indent=''):
		print(indent, repr(self), sep='')

		for child in self.children:
			child.tree(indent + '    ')

	def _normpath(self, parent):
		for child in self._get_collection().find({'t_a._id': parent}, {'n': 1, 't_a.n': 1}).sort('t_P'):
			self.tqs(id=child['_id']).update_one(set__path='/' + '/'.join(chain((i['n'] for i in child['t_a']), [child['n']])))

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
		self.tqs(id=self.id).replace(source)
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
