# encoding: utf-8

from re import escape
from pathlib import PurePosixPath
from itertools import chain
from pymongo.errors import BulkWriteError

from marrow.mongo import Document, Field, Index, U
from marrow.mongo.field import Array, Embed, String, Path, PluginReference, Reference, ObjectId, Translated
from marrow.mongo.trait import Derived, Localized, Published, Queryable, Identified


log = __import__('logging').getLogger(__name__)


class _Resolver(Document):
	plugin = PluginReference(namespace='web.component.model')


class Asset(Derived, Localized, Published, Queryable):
	"""The definition of a Contentment Asset.
	
	This is the primary mechanism of dispatch, that is, looking up the handler for a given resource. To facilitate
	this the Asset model contains the security information, taxonomy, and basic metadata. The abstract properties
	feature is meant for user annotation, not technical use. Technical use should utilize proper fields declared
	in Asset subclasses.
	
	Bare assets are often utilized as containers for other, more richly described assets such as pages.
	"""
	
	# Database Metadata
	
	__database__ = 'default'
	__collection__ = 'asset'
	__icon__ = 'folder-o'
	
	# Embedded Documents
	
	class Locale(Localized.Locale):
		"""Language-dependent Asset content."""
		
		title = String()
		description = String()
	
	class Property(Document):
		__pk__ = 'name'
		
		name = String()
		value = Field()
		language = String(default=None)
	
	# Fields
	
	id = ObjectId('_id', assign=True, write=False, repr=False, positional=False)
	parent = Reference('.', default=None, assign=True)  # Required for fast immediate child lookups; not infrequent.
	path = Path(required=True)  # Required for fast path enumeration and parents/descendants lookups; most frequent.
	dependent = Array(Reference('.'), assign=True)  # Other assets which depend on this one. Used for cache updates.
	
	title = Translated('title')
	description = Translated('description')
	
	acl = Array(Embed('ACLRule'), assign=True)  # Security predicates applicable to this Asset.
	tag = Array(String(), assign=True)  # TODO: Set field.
	attr = Array(Embed(Property), assign=True)
	
	handler = PluginReference('web.component', default=None)
	
	# Indexes
	
	_text = Index('$tags', '$locale.title', '$locale.description')
	_parent = Index('parent')
	_path = Index('path', unique=True)
	_property = Index('property.name', 'property.value')
	
	# Related Query Fragment Generators
	
	def children(self):
		"""Query fragment selecting immediate children."""
		
		return Asset.parent == self
	
	def parents(self):
		"""A query fragment selecting parents """
		
		return Asset.path.any(self.path.parents)
	
	def descendants(self):
		"""Query fragment selecting children of all depths."""
		
		return Asset.path.re(r'^', escape(str(self.path)), r'\/')
	
	# Queryable Helpers
	
	def get_nearest(self, path, base=None):
		"""Find and return the deepest Asset matching the given path."""
		
		path = PurePosixPath(path)
		
		return self.find_one(path__in=chain((path, ), path.parents), sort=('-path', ))
	
	def find_nearest(self, path, *args, **kw):
		"""Find all nodes up to the deepest node matched by the given path.
		
		Conceptually the reverse of `get_nearest`.
		"""
		
		path = PurePosixPath(path)
		
		for doc in self.find(*args, path__in=chain((path, ), path.parents), sort=('path', ), **kw):
			yield self.from_mongo(doc)
	
	def attach(self, parent):
		"""Attach this asset (and any descendants) to another parent."""
		
		if not isinstance(parent, Asset):
			parent = Asset.find_one(parent, project=('path', ))
		
		descendants = self.find(self.descendants, project=('path', ))
		length = len(str(self.path.parent)) + 1  # We use simplified string manipulation to calculate updated paths.
		ops = self.get_collection().initialize_unordered_bulk_op()
		
		# Update ourselves.
		ops.find(Asset.id == self).update_one(U(Asset, parent=parent, path=parent.path / self.path.name))
		
		# Update descendants, if any.
		for offspring in descendants:
			opath = parent.path / offspring['path'][length:]
			ops.find(Asset.id == offspring).update_one(U(Asset, path=opath))
		
		# Alas, we can't sensibly reach other records, such as any loaded copies of descendants, to update them.
		self.parent = parent  # Assign a local copy for convienence sake.
		self.path = parent.path / self.path.name  # Also assign the updated path.
		
		try:  # TODO: Better error handling.
			ops.execute()
		except BulkWriteError as e:
			__import__('pprint').pprint(e.details)
			raise
		
		return self
	
	# Data Interoperability
	# from/to_json are provided by Document
	
	def from_xml(self, content, context=None):
		pass
	
	def to_xml(self, context=None):
		pass
	
	# Python Protocols
	
	def __init__(self, *args, **kw):
		if args:
			if 'path' in kw:
				raise TypeError("Can not define positional name and keyword path simultaneously.")
			
			kw['path'], *args = args
		
		super(Asset, self).__init__(*args, **kw)
	
	# Contentment Protocols
	
	@property
	def __link__(self):
		component = _Resolver(self.__class__)['plugin']
		return 'asset:{component}:{identifier!s}'.format(component=component, identifier=self.id)
	
	def __depends__(self, context):
		"""Identify the elements required for this asset to function.
		
		This may identify CSS, JS, or other Asset dependencies.
		"""
		
		pass
	
	def __html__(self):
		"""Return the rendered HTML version of this asset."""
		
		buffer = []
		context = {}
		
		for chunk in self.__embed__(context):
			if not chunk:
				continue
			
			if hasattr(chunk, 'result'):
				chunk = chunk.result()  # We don't mess around with deferred chunks at this level.
			
			buffer.append(chunk)
		
		return "".join(buffer)
	
	def __html_format__(self, spec=None):
		"""Special handler for use in MarkupSafe formatting and %{} cinje replacements.
		
		For example:
		
			%{"{:link}" some_page}
		
		"""
		
		if spec == 'link':
			return self.path
		
		if spec == 'urn':
			return self.__link__
		
		elif spec:
			raise ValueError("Invalid format specification for Asset: " + spec)
		
		return self.__html__()
	
	def __stream__(self, context):
		"""Produce a mixed cinje content and component stream representing the "rendered" form of this asset."""
		
		yield None
	
	def __embed__(self, context):
		"""Produce a pure cinje content stream representing the "embedded" form of this asset.
		
		Assets (components) emitted by `__stream__` will be embedded.
		"""
		
		yield None
	
	def __present__(self, context):
		"""Perform any work useful prior to presentation of this object by the back-end.
		
		This can be used to assign appropriate last-modified and cache control headers, amongst other uses.
		"""
		
		context.response.last_modified = self.modified
	
	def __panel__(self, context):
		"""Yield a component stream of tiles to add to management panels."""
		
		pass
