# encoding: utf-8

from functools import partial

from marrow.mongo import Document, Field, Index
from marrow.mongo.field import Array, Embed, String, PluginReference, Reference, Translated, Set
from marrow.mongo.trait import Derived, Localized, Published, Queryable, HPath, HParent


log = __import__('logging').getLogger(__name__)


class classinstancemethod:
	"""A decorator to allow protocol methods to behave as class and instance methods."""
	
	def __init__(self, fn):
		self.fn = staticmethod(fn)
	
	def __get__(self, obj, cls=None):
		# There's probably a way, way, way better way of doing this!
		return partial(self.fn, cls if obj is None else obj)
	
	def __set__(self, obj, value):
		raise TypeError("Dual class/instance methods can not be written to.")



class _Resolver(Document):
	plugin = PluginReference(namespace='web.component')


class Asset(Derived, Localized, Published, HPath, HParent, Queryable):
	"""The definition of a Contentment Asset.
	
	This is the primary mechanism of dispatch, that is, looking up the handler for a given resource. To facilitate
	this the Asset model contains the security information, taxonomy, and basic metadata. The abstract properties
	feature is meant for user annotation, not technical use. Technical use should utilize proper fields declared
	in Asset subclasses.
	
	Bare assets are often utilized as containers for other, more richly described assets such as pages.
	
	Subclasses are used to override defaults (such as the handler) and add new data model properties appropriate for
	the derived type. For example, a very simple Page might define its contents as a String field. Some Asset
	derivitives may define no new fields at all. This serves two purposes: handler default assignment, and
	clear specification of the object to reference when loading the record, indirectly through assignment to `cls`.
	
	Additionally, subclasses are expected to populate a number of Contentment protocol methods and properties.
	"""
	
	# Database Metadata
	
	__database__ = 'default'
	__collection__ = 'asset'
	
	# Dependency Declaration
	
	class Depend:
		NS = 'org.python.setuptools.entry_point'
		PLUGIN = 'org.marrow.package.load'
		ASSET = 'web.component.asset'
		BUNDLE = 'web.asset.bundle'
		STYLE = 'web.asset.selector'
		EVENT = 'web.asset.event'
		
		ALL = (NS, PLUGIN, ASSET, BUNDLE, STYLE, EVENT)
		
		@classmethod
		def collect(cls, obj, *only):
			if not only:
				only = cls.ALL
			
			yield from obj.__depend__(obj, only)
		
		@classmethod
		def declare(cls, fn):
			return classinstancemethod(fn)
	
	# Embedded Documents
	
	class Locale(Localized.Locale):
		"""Language-dependent Asset content."""
		
		# This is a magical property to store "additional full text content" extracted from rich assets.
		text = String('_text', project=False, read=False, write=False, repr=False, positional=False)
		
		title = String()
		description = String()
	
	class Property(Document):
		__pk__ = 'name'
		
		name = String()
		value = Field()
		language = String(default=None)
	
	# Fields
	
	id = HParent.id.adapt(positional=False)
	dependent = Array(Reference('.'), assign=True)  # Other assets which depend on this one. Used for cache updates.
	
	title = Translated('title')
	description = Translated('description')
	
	acl = Array(Embed('ACLRule'), assign=True)  # Security predicates applicable to this Asset.
	tag = Set(String(), assign=True)
	attr = Array(Embed('.Property'), assign=True)
	
	handler = PluginReference('web.component.${cls.__name__}', default='default')
	
	# Indexes
	
	_text = Index('$tags', '$locale.title', '$locale.description')
	_parent = Index('parent')
	_path = Index('path', unique=True)
	_property = Index('property.name', 'property.value')
	
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
	
	__vary__ = ('id', 'modified')  # The attributes to fetch for cache key generation.
	
	def __link__(self):
		component = _Resolver(self.__class__)['plugin']
		return 'asset:{identifier!s}'.format(component=component, identifier=self.id)
	
	@classinstancemethod
	def __depends__(self, only):
		"""Identify the elements required for this asset to function.
		
		This may declare static asset bundle dependencies, theme selectors, event names, other assets, etc.
		
		Falsy (e.g. `None`) values will be ignored by the collector and are safe (if silly) to provide.
		"""
		
		D = self.Depend
		handler = self.__class__.handler
		
		if D.NS in only:  # Declare namespaces we utilize plugins from.
			yield D.NS, handler.namespace
		
		if D.PLUGIN in only:  # Declare explicit plugins (or dot-colon import paths) we utilize.
			# We need to avoid typecasting on dereferencing... and explosion noises.
			
			if ~handler in self or handler.default:
				yield D.PLUGIN, handler.namespace, self.get(~handler, handler.default)
		
		if D.BUNDLE in only:
			yield D.BUNDLE, 'web.component.asset'
		
		if D.ASSET in only:  # Declare other Assets this one directly depends upon.
			yield D.ASSET, self.parent  # Might, in some rare circumstances, actually be None. Whoops!
	
	def __text__(self):
		"""Yield additional chunks of optionally language-dependent textual content to full-text index."""
		
		return
		yield
	
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
			return self.__link__()
		
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
