# encoding: utf-8

from itertools import chain

from bson import ObjectId
from mongoengine import QuerySet, Q
from mongoengine import Document, ListField, StringField, IntField
from mongoengine import CachedReferenceField
from mongoengine.fields import RECURSIVE_REFERENCE_CONSTANT
from mongoengine.signals import pre_delete

from .util.model import signal

log = __import__('logging').getLogger(__name__)


@signal(pre_delete)
def remove_children(sender, document, **kw):
	document.empty()


class TaxonomyQuerySet(QuerySet):
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
		"""Add an asset, specified by the parameter, as a child of the currently selected assets."""

		objs = self.clone().scalar('id')
		obj = objs[0]

		log.info("Inserting asset.", extra=dict(asset=obj, index=index, child=getattr(child, 'id', child)))

		# Detach the new child (and thus it's own child nodes).
		child = (self._document.objects.get(id=child) if isinstance(child, ObjectId) else child).detach(False)

		if index < 0:
			_max = self._document.objects(parent=obj).order_by('-order').scalar('order').first()
			index = 0 if _max is None else (_max + 1)

		self._document.objects(parent=obj, order__gte=index).update(inc__order=1)

		log.debug("before", extra=dict(data=repr(child._data)))

		child.order = index

		child.path = obj.path + '/' + child.name
		child.parent = obj
		child.parents = list(obj.parents)
		child.parents.append(obj)

		log.debug("after", extra=dict(data=repr(child._data)))

		child = child.save()

		ancestors = list(self._document.objects(id=child.id).scalar('parents').no_dereference())
		print("Child contents:", child.contents)
		child.contents.update(__raw__={'$push': {'t_a': {'$each': ancestors, '$position': 0}}})
		# child.contents.update(push__ancestors={'$each': ancestors, '$position': 0})  # Unimplemented.

		self._normpath(child.id)

		return self

	def detach(self, path=True):
		"""Detach this asset from its current taxonomy."""

		objs = self.clone().scalar('id')
		obj = objs[0]

		if obj.path in (None, '', obj.name):
			return self

		self.nextAll.update(inc__order=-1)

		self.contents.update(parents__pull_all=obj.parents)

		self.order = None
		self.path = self.name
		self.parent = None
		del self.parents[:]

		if path:
			self._normpath(self.id)
			return self.save()

		return self

	def append(self, child):
		"""Insert an asset, specified by the parameter, as a child of this asset."""
		return self

		#return self.insert(-1, child)

	def prepend(self, child):
		return self

		#return self.insert(0, child)

	def after(self, sibling):
		"""Insert an asset, specified by the parameter, after this asset."""
		return self

		#self.parent.insert(self.order + 1, sibling)
		#return self.reload()

	def before(self, sibling):
		"""Insert an asset, specified by the parameter, before this asset."""
		return self

		#self.parent.insert(self.order, sibling)
		#return self.reload()

	def replace(self, target):
		"""Replace an asset, specified by the parameter, with this asset."""
		return self

		#target = self.__rcls__.objects.get(id=target) if isinstance(target, ObjectId) else target

		#self.name = target.name
		#self.parent = target.parent
		#self.parents = target.parents
		#self.path = target.path
		#self.order = target.order

		#target.delete()

		#return self.save()

	def replaceWith(self, source):
		"""Replace this asset with an asset specified by the parameter."""
		return self

		#source = self.__rcls__.objects.get(id=source) if isinstance(source, ObjectId) else source

		#source.name = self.name
		#source.parent = self.parent
		#source.parents = self.parents
		#source.path = self.path
		#source.order = self.order

		#self.delete()

		#return source.save()

	def clone(self):
		return self
		#clone = self.__rcls__.objects.get(id=self.id)
		#del clone.id
		#return clone

	# Pivoted Manipulation

	def appendTo(self, parent):
		"""Insert this asset as a child of the asset specified by the parameter."""
		return self
		#parent = self.__rcls__.objects(pk=parent).get() if isinstance(parent, ObjectId) else parent
		#parent.append(self)
		#return self.reload()

	def prependTo(self, parent):
		"""Insert this asset as the left-most child of the asset specified by the parameter."""
		return self
		#parent = self.__rcls__.objects(pk=parent).get() if isinstance(parent, ObjectId) else parent
		#parent.prepend(self)
		#return self.reload()

	def insertBefore(self, sibling):
		"""Insert this asset as the left-hand sibling of the asset specified by the parameter."""
		return self
		#sibling = self.__rcls__.objects(pk=sibling).get() if isinstance(sibling, ObjectId) else sibling
		#sibling.before(self)
		#return self.reload()

	def insertAfter(self, sibling):
		"""Insert his asset as the right-hand child of the asset specified by the parameter."""
		return self
		#sibling = self.__rcls__.objects(pk=sibling).get() if isinstance(sibling, ObjectId) else sibling
		#sibling.after(self)
		#return self.reload()

	# Traversal

	@property
	def children(self):
		"""Yield all direct children of this asset."""

		return self._document.objects(parent__in=list(self.clone().scalar('id'))).order_by('parent', 'order')

	@property
	def contents(self):
		"""Yield all descendants of this asset."""

		return self._documnet.objects(parents__in=self.clone().scalar('id').all()).order_by('parent', 'order')

	@property
	def siblings(self):
		"""All siblings of the currently selected assets, not including these assets."""
		from operator import __or__
		from functools import reduce

		query = []

		for parent, order in self.clone().only('parent', 'order').no_dereference():
			query.append(Q(parent=parent, order__ne=order, id__ne=order))

		if not query:  # TODO: Armour everywhere.
			return None

		return self._document.objects(reduce(__or__, query)).order_by('parent', 'order')

	@property
	def next(self):
		"""The sibling immediately following this asset."""
		from operator import __or__
		from functools import reduce

		query = []

		for parent, order in self.clone().only('parent', 'order').no_dereference():
			query.append(Q(parent=parent, order=order + 1))

		return self._document.objects(reduce(__or__, query)).order_by('path')

	@property
	def nextAll(self):
		"""All siblings following this asset."""
		from operator import __or__
		from functools import reduce

		query = []

		# Indexing note: (parent, order, id) for covered query and optimal re-use.
		# Including id here to prevent an edge case (assets being shuffled) from including non-siblings.
		for id, parent, order in self.clone().only('id', 'parent', 'order').no_dereference():
			query.append(Q(parent=parent, order__gt=order, id__ne=id))

		return self._document.objects(reduce(__or__, query)).order_by('parent', 'order')

	@property
	def prev(self):
		"""The sibling immediately preceeding this asset."""
		from operator import __or__
		from functools import reduce

		query = []

		for parent, order in self.clone().only('parent', 'order').no_dereference():
			query.append(Q(parent=parent, order=order - 1))

		return self._document.objects(reduce(__or__, query)).order_by('parent')

	@property
	def prevAll(self):
		"""All siblings preceeding the selected assets."""

		from operator import __or__
		from functools import reduce

		query = []

		for parent, order in self.clone().only('parent', 'order').no_dereference():
			query.append(Q(parent=parent, order__lt=order))

		return self._document.objects(reduce(__or__, query)).order_by('parent', 'order')

	def contains(self, other):
		"""The asset, specified by the parameter, is a descendant of any of the selected assets."""

		if __debug__:  # Can be optimized away (-O) in production.
			from web.component.asset import Asset
			assert isinstance(other, Asset) or isinstance(other, ObjectId), "Argument must be Asset or ObjectId instance."

		return other._data['parent'].id if hasattr(other, '_data') else other in self.scalar('id')

	def extend(self, *others):
		"""Merge the contents of another asset or assets, specified by positional parameters, with this one."""
		return self
		for other in others:
			for child in other.children:
				self.insert(-1, child)


class Taxonomy(Document):
	meta = dict(
		ordering = ['order'],
		allow_inheritance = True,
		queryset_class = TaxonomyQuerySet,
	)

	parent = CachedReferenceField(
			'Taxonomy',
			db_field = 't_p',
			fields = ['name'],
			export=False
		)
	parents = ListField(CachedReferenceField(
			'Taxonomy',
			fields = ['name', 'acl'],
		), db_field='t_a', export=False)

	name = StringField(db_field='n', export=True, simple=True)
	path = StringField(db_field='t_P', unique=True, export=True, simple=True)
	order = IntField(db_field='t_o', default=0, export=True, simple=True)

	def __repr__(self):
		return "{0.__class__.__name__} ({0.name}, {0.path})".format(self)

	def tree(self, indent=''):
		print(indent, repr(self), sep='')

		for child in self.children:
			child.tree(indent + '    ')

	def _normpath(self, parent):
		for child in self._get_collection().find({'t_a._id': parent}, {'n': 1, 't_a.n': 1}).sort('t_P'):
			self._qs(id=child['_id']).update_one(set__path='/' + '/'.join(chain((i['n'] for i in child['t_a']), [child['n']])))

	def empty(self):
		self._qs(id=self.id).empty()

	def detach(self, path=True):
		"""Detach this asset from its current taxonomy."""

		if self.path in (None, '', self.name):
			return self

		log.warn("Detaching from taxonomy." + "\n\t" + __import__('json').dumps(dict(asset=repr(self), path=path)))

		self.nextAll.update(inc__order=-1)

		self.contents.update(parents__pull_all=self.parents)

		self.order = None
		self.path = self.name
		self.parent = None
		del self.parents[:]

		if path:
			self._normpath(self.id)
			return self.save()

		return self

	def insert(self, index, child):
		"""Add an asset, specified by the parameter, as a child of this asset."""

		log.info("Inserting asset.", extra=dict(asset=self.id, index=index, child=getattr(child, 'id', child)))

		# Detach the new child (and thus it's own child nodes).
		child = (self._qs.get(id=child) if isinstance(child, ObjectId) else child).detach(False)

		if index < 0:
			_max = self._qs(parent=self).order_by('-order').scalar('order').first()
			index = 0 if _max is None else (_max + 1)

		self._qs(parent=self, order__gte=index).update(inc__order=1)

		log.debug("before", extra=dict(data=repr(child._data)))

		child.order = index

		child.path = self.path + '/' + child.name
		child.parent = self
		child.parents = list(self.parents)
		child.parents.append(self)

		log.debug("after", extra=dict(data=repr(child._data)))

		child = child.save()

		ancestors = list(self._qs(id=child.id).scalar('parents').no_dereference())
		ancestors = [[a.id for a in ancs] for ancs in ancestors]
		print("Child contents:", child.contents)
		child.contents.update(__raw__={'$push': {'t_a': {'$each': ancestors, '$position': 0}}})
		# child.contents.update(push__ancestors={'$each': ancestors, '$position': 0})  # Unimplemented.

		self._normpath(child.id)

		return self

	def append(self, child):
		"""Insert an asset, specified by the parameter, as a child of this asset."""
		return self.insert(-1, child)

	def prepend(self, child):
		return self.insert(0, child)

	def after(self, sibling):
		"""Insert an asset, specified by the parameter, after this asset."""
		self.parent.insert(self.order + 1, sibling)
		return self.reload()

	def before(self, sibling):
		"""Insert an asset, specified by the parameter, before this asset."""
		self.parent.insert(self.order, sibling)
		return self.reload()

	def replace(self, target):
		"""Replace an asset, specified by the parameter, with this asset."""

		target = self._qs.get(id=target) if isinstance(target, ObjectId) else target

		self.name = target.name
		self.parent = target.parent
		self.parents = target.parents
		self.path = target.path
		self.order = target.order

		target.delete()

		return self.save()

	def replaceWith(self, source):
		"""Replace this asset with an asset specified by the parameter."""

		source = self._qs.get(id=source) if isinstance(source, ObjectId) else source

		source.name = self.name
		source.parent = self.parent
		source.parents = self.parents
		source.path = self.path
		source.order = self.order

		self.delete()

		return source.save()

	def clone(self):
		clone = self._qs.get(id=self.id)
		del clone.id
		return clone

	def appendTo(self, parent):
		"""Insert this asset as a child of the asset specified by the parameter."""

		parent = self._qs(pk=parent).get() if isinstance(parent, ObjectId) else parent
		parent.append(self)

		return self.reload()

	def prependTo(self, parent):
		"""Insert this asset as the left-most child of the asset specified by the parameter."""

		parent = self._qs(pk=parent).get() if isinstance(parent, ObjectId) else parent
		parent.prepend(self)

		return self.reload()

	def insertBefore(self, sibling):
		"""Insert this asset as the left-hand sibling of the asset specified by the parameter."""

		sibling = self._qs(pk=sibling).get() if isinstance(sibling, ObjectId) else sibling
		sibling.before(self)

		return self.reload()

	def insertAfter(self, sibling):
		"""Insert his asset as the right-hand child of the asset specified by the parameter."""

		sibling = self._qs(pk=sibling).get() if isinstance(sibling, ObjectId) else sibling
		sibling.after(self)

		return self.reload()

	@property
	def children(self):
		"""Yield all direct children of this asset."""
		return self._qs(__raw__={'t_p._id': self.id}).order_by('order')

	@property
	def contents(self):
		"""Yield all descendants of this asset."""
		return self._qs(parents=self).order_by('path')

	@property
	def contents(self):
		"""Yield all descendants of this asset."""
		return self._qs(parents=self).order_by('path')

	@property
	def siblings(self):
		"""All siblings of this asset, not including this asset."""
		return self._qs(parent=self.parent, id__ne=self.id).order_by('order')

	@property
	def next(self):
		"""The sibling immediately following this asset."""
		return self._qs(parent=self.parent, order__gt=self.order).order_by('order').first()

	@property
	def nextAll(self):
		"""All siblings following this asset."""
		return self._qs(parent=self.parent, order__gt=self.order).order_by('order')

	@property
	def prev(self):
		"""The sibling immediately preceeding this asset."""
		return self._qs(parent=self.parent, order__lt=self.order).order_by('-order').first()

	@property
	def prevAll(self):
		"""All siblings preceeding this asset."""
		return self._qs(parent=self.parent, order__lt=self.order).order_by('order')

	def contains(self, other):
		"""The asset, specified by the parameter, is a descendant of this asset."""
		return bool(self._qs(pk=self.pk, children=other).count())

	def extend(self, *others):
		"""Merge the contents of another asset or assets, specified by positional parameters, with this one."""

		for other in others:
			for child in other.children:
				self.insert(-1, child)
