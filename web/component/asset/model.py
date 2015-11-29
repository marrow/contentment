# encoding: utf-8

from bson import ObjectId

from marrow.package.cache import PluginCache
from mongoengine import Document
from mongoengine import EmbeddedDocumentField
from mongoengine import StringField, IntField, MapField, DateTimeField, CachedReferenceField, ListField

from web.contentment.acl import ACLRule
from web.contentment.taxonomy import remove_children, TaxonomyQuerySet
from web.contentment.util import utcnow, D_
from web.contentment.util.model import update_modified_timestamp, Properties as P
#from web.contentment.okapi import update_full_text_index, remove_full_text_index, Indexed
from web.component.asset.xml import templates, importers

log = __import__('logging').getLogger(__name__)


#@update_full_text_index.signal
#@remove_full_text_index.signal
@remove_children.signal
@update_modified_timestamp.signal
class Asset(Document):
	meta = dict(
			collection = 'asset',
			ordering = ['order'],
			allow_inheritance = True,
			queryset_class = TaxonomyQuerySet,
			index_cls = False,
			
			# TODO: Bug in MongoEngine?
			#indexes = [
			#		'path',
			#		('parent', 'order', 'id'),
			#		'parents',
			#	],
		)
	
	__fulltext__ = dict(title=10.0, description=5.0, tags=8.5)
	__icon__ = 'folder-o'

	__xml_exporters__ = dict(
		title = templates.translated_field,
		description = templates.translated_field,
	)

	__xml_importers__ = dict(
		title = importers.translated_field,
		description = importers.translated_field,
	)
	
	# Taxonomy
	
	parent = CachedReferenceField(
			'Asset',
			db_field = 't_p',
			fields = ['name'],
			custom_data=P(export=False),
		)
	parents = ListField(CachedReferenceField(
			'Asset',
			fields = ['name', 'acl'],
		), db_field='t_a', custom_data=P(export=False))
	
	name = StringField(db_field='n', custom_data=P(export=True, simple=True))
	path = StringField(db_field='t_P', unique=True, custom_data=P(export=True, simple=True))
	order = IntField(db_field='t_o', default=0, custom_data=P(export=True, simple=True))
	
	# Basic Properties
	title = MapField(StringField(), db_field='a_t', default=dict, custom_data=P(export=True, simple=False))  # TODO: TranslatedField
	description = MapField(StringField(), db_field='a_d', default=dict, custom_data=P(export=True, simple=False))  # TODO: TranslatedField
	tags = ListField(StringField(), db_field='a_T', default=list, custom_data=P(export=True, simple=True))
	
	# Magic Properties
	properties = EmbeddedDocumentField(P, db_field='a_p', default=P, custom_data=P(export=True, simple=False), verbose_name='property')
	acl = ListField(EmbeddedDocumentField(ACLRule), db_field='a_a', default=list, custom_data=P(export=True, simple=False))
	handler = StringField(db_field='a_h', custom_data=P(export=True, simple=True))  # TODO: PythonReferenceField('web.component') | URLPath allowing relative
	
	# Metadata
	created = DateTimeField(db_field='a_dc', default=utcnow, custom_data=P(export=True, simple=False))
	modified = DateTimeField(db_field='a_dm', default=utcnow, custom_data=P(export=True, simple=False))

	# Controller Lookup
	
	_controller_cache = PluginCache('web.component')
	
	@property
	def controller(self):  # TODO: Move this into PythonReferencefield.
		if not self.handler:
			return self, self._controller_cache['web.component.asset:AssetController']
		
		if ':' in self.handler:
			return self, self._controller_cache[self.handler]
		
		handler = self.children.named(self.handler).get()
		return handler.controller
	
	# Python Methods
	
	def __str__(self):
		return D_(self.title)
	
	def __repr__(self):
		return "{0.__class__.__name__}({2}, {1!r}, {0.handler}, {0.properties!r})".format(self, D_(self.title), self.path or self.name)
	
	# Visualization
	
	def tree(self, indent=''):
		print(indent, repr(self), sep='')
		
		for child in self.children:
			child.tree(indent + '    ')
	
	# Data Portability
	
	def __xml__(self, recursive=False):
		"""Return an XML representation for this Asset."""

		yield from templates.asset(self, recursive, root=True)

	as_xml = property(lambda self: self.__xml__(recursive=False))
	
	def __json__(self):
		"""Return a JSON-safe (and YAML-safe) representation for this Asset."""
		return dict(
				id = str(self.id),
				title = self.title,
				description = self.description,
				tags = [i for i in self.tags if ':' not in i],
				created = self.created,
				modified = self.modified
			)
	
	as_json = property(lambda self: self.__json__())
	
	def __html_stream__(self):
		"""Return a cinje-compatible template representing the HTML version of this Asset."""
		return []
	
	as_stream = property(lambda self: self.__html_stream__)  # Note: doesn't call!
	
	def __html__(self):
		"""Return the rendered HTML representation of this Asset."""
		return "".join(self.__html_stream__())
	
	as_html = property(lambda self: self.__html__())
	
	def __html_format__(self, spec=None):
		"""Special handler for use in MarkupSafe formatting and %{} cinje replacements.
		
		For example:
		
			%{"{:link}" some_page}
		
		"""
		
		if spec == 'link':
			return self.path
		
		elif spec:
			raise ValueError("Invalid format specification for Asset: " + spec)
		
		return self.__html__()
	
	def __text__(self):
		"""Return the full content of the page as a single block of text.
		
		This is principally used for full-text content extraction as part of the indexing process.
		"""
		return ""
	
	as_text = property(lambda self: self.__text__())
	
	# Taxonomy
	
	# Internal Management
	
	def _normpath(self, parent):
		for child in self._get_collection().find({'t_a._id': parent}, {'n': 1, 't_a.n': 1}).sort('t_P'):
			Asset.objects(id=child['_id']).update_one(set__path='/' + '/'.join(chain((i['n'] for i in child['t_a']), [child['n']])))
	
	# Basic Management
	
	def empty(self):
		"""Delete all descendants of this asset."""
		log.warn("Emptying asset of children.", extra=dict(asset=self.id))
		# "only" here is an optimization to speed up signal delivery
		self.children.only('id').delete(_from_doc_delete=True)
		return self
	
	def insert(self, index, child):
		"""Add an asset, specified by the parameter, as a child of this asset."""
		
		log.info("Inserting asset.", extra=dict(asset=self.id, index=index, child=getattr(child, 'id', child)))
		
		# Detach the new child (and thus it's own child nodes).
		child = (Asset.objects.get(id=child) if isinstance(child, ObjectId) else child).detach(False)
		
		if index < 0:
			_max = Asset.objects(parent=self).order_by('-order').scalar('order').first()
			index = 0 if _max is None else (_max + 1)
		
		Asset.objects(parent=self, order__gte=index).update(inc__order=1)
		
		log.debug("before", extra=dict(data=repr(child._data)))
		
		child.order = index
		
		child.path = self.path + '/' + child.name
		child.parent = self
		child.parents = list(self.parents)
		child.parents.append(self)
		
		log.debug("after", extra=dict(data=repr(child._data)))
		
		child = child.save()
		
		ancestors = list(Asset.objects(id=child.id).scalar('parents').no_dereference())
		print("Child contents:", child.contents)
		child.contents.update(__raw__={'$push': {'t_a': {'$each': ancestors, '$position': 0}}})
		# child.contents.update(push__ancestors={'$each': ancestors, '$position': 0})  # Unimplemented.
		
		self._normpath(child.id)
		
		return self
	
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
		
		target = Asset.objects.get(id=target) if isinstance(target, ObjectId) else target
		
		self.name = target.name
		self.parent = target.parent
		self.parents = target.parents
		self.path = target.path
		self.order = target.order
		
		target.delete()
		
		return self.save()
	
	def replaceWith(self, source):
		"""Replace this asset with an asset specified by the parameter."""
		
		source = Asset.objects.get(id=source) if isinstance(source, ObjectId) else source
		
		source.name = self.name
		source.parent = self.parent
		source.parents = self.parents
		source.path = self.path
		source.order = self.order
		
		self.delete()
		
		return source.save()
	
	def clone(self):
		clone = Asset.objects.get(id=self.id)
		del clone.id
		return clone
	
	# Pivoted Manipulation
	# These are actually implemented elsewhere.
	
	def appendTo(self, parent):
		"""Insert this asset as a child of the asset specified by the parameter."""
		
		parent = Asset.objects(pk=parent).get() if isinstance(parent, ObjectId) else parent
		parent.append(self)
		
		return self.reload()
	
	def prependTo(self, parent):
		"""Insert this asset as the left-most child of the asset specified by the parameter."""
		
		parent = Asset.objects(pk=parent).get() if isinstance(parent, ObjectId) else parent
		parent.prepend(self)
		
		return self.reload()
	
	def insertBefore(self, sibling):
		"""Insert this asset as the left-hand sibling of the asset specified by the parameter."""
		
		sibling = Asset.objects(pk=sibling).get() if isinstance(sibling, ObjectId) else sibling
		sibling.before(self)
		
		return self.reload()
	
	def insertAfter(self, sibling):
		"""Insert his asset as the right-hand child of the asset specified by the parameter."""
		
		sibling = Asset.objects(pk=sibling).get() if isinstance(sibling, ObjectId) else sibling
		sibling.after(self)
		
		return self.reload()
	
	# Traversal
	
	@property
	def children(self):
		"""Yield all direct children of this asset."""
		return Asset.objects(__raw__={'t_p._id': self.id}).order_by('order')
	
	@property
	def contents(self):
		"""Yield all descendants of this asset."""
		return Asset.objects(parents=self).order_by('path')
	
	@property
	def siblings(self):
		"""All siblings of this asset, not including this asset."""
		return Asset.objects(parent=self.parent, id__ne=self.id).order_by('order')
	
	@property
	def next(self):
		"""The sibling immediately following this asset."""
		return Asset.objects(parent=self.parent, order__gt=self.order).order_by('order').first()
	
	@property
	def nextAll(self):
		"""All siblings following this asset."""
		return Asset.objects(parent=self.parent, order__gt=self.order).order_by('order')
	
	@property
	def prev(self):
		"""The sibling immediately preceeding this asset."""
		return Asset.objects(parent=self.parent, order__lt=self.order).order_by('-order').first()
	
	@property
	def prevAll(self):
		"""All siblings preceeding this asset."""
		return Asset.objects(parent=self.parent, order__lt=self.order).order_by('order')
	
	def contains(self, other):
		"""The asset, specified by the parameter, is a descendant of this asset."""
		return bool(Asset.objects(pk=self.pk, children=other).count())
	
	def extend(self, *others):
		"""Merge the contents of another asset or assets, specified by positional parameters, with this one."""
		
		for other in others:
			for child in other.children:
				self.insert(-1, child)
