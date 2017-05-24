# encoding: utf-8

from cinje.util import interruptable
from marrow.mongo import Document, Field, Index
from marrow.mongo.field import Array, Embed, String, Path, PluginReference, Reference, Translated, Integer, Set
from marrow.mongo.trait import Derived, Localized, Published, Queryable, HPath, HParent


log = __import__('logging').getLogger(__name__)


class _Resolver(Document):
	plugin = PluginReference(namespace='web.component')


class Asset(Derived, Localized, Published, HPath, HParent):
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
	
	id = HParent.id.adapt(positional=False)
	dependent = Array(Reference('.'), assign=True)  # Other assets which depend on this one. Used for cache updates.
	
	title = Translated('title')
	description = Translated('description')
	
	acl = Array(Embed('ACLRule'), assign=True)  # Security predicates applicable to this Asset.
	tag = Set(String(), assign=True)
	attr = Array(Embed('.Property'), assign=True)
	
	handler = PluginReference('web.component', default=None)
	
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


class Style(Document):
	# Template engine stuff.
	container = PluginReference(default=None)  # The cinje wrapping template to use.
	attributes = Embed(Document, default=None)  # Arguments to the cinje wrapping template.
	
	# CSS stuff.
	identifier = String(default=None)  # The HTML identifier.
	classes = Set(String(), assign=True)  # CSS classes applied.
	
	# Theme stuff.
	selectors = Array(Embed(Asset.Property), assign=True)  # CSS selector mappings.


class Page(Asset):
	related = Array(Reference(Asset), assign=True)
	template = Reference(Asset, default=None)
	style = Embed(Style, assign=True)
	
	handler = Asset.handler.adapt(default='org.contentment.page.default')
	
	def blocks(self):
		# from marrow.mongo.document import Block
		return Block.blocks_for(self)
	
	def __embed__(self, context):
		container = self.style.container
		
		if container:  # Given a wrapping container template, stream the prefix.
			kw = dict(self.style.attributes) if self.style.attributes else {}
			kw.setdefault('id', str(self.id))
			container = container(context, **kw)
			
			yield from interruptable(container)
		
		for block in self.blocks:
			yield from block.__embed__(context)
		
		if container:  # Yield the remainder (postfix) of the wrapping template.
			yield from container


class Block(Derived, Queryable):
	__database__ = 'default'
	__collection__ = 'block'
	
	class Placement(Document):
		page = Reference(Page)
		position = Integer(default=None)
	
	language = String(default=None)
	places = Array(Embed('.Placement'), assign=True)  # The Page instances this block is utilized within.
	
	acl = Array(Embed('ACLRule'), assign=True)  # Security predicates applicable to this block.
	tag = Set(String(), assign=True)
	attr = Array(Embed(Asset.Property), assign=True)
	
	_place = Index('places.page', 'language', 'places.position', unique=True)  # Two objects may not occupy the same space.
	
	@classmethod
	def blocks_for(cls, page, language=None):
		q = cls.places.page == page
		
		if language:
			q &= cls.language == language
		
		for record in cls.find(q, sort=('places__S__position', )):
			yield cls.from_mongo(record)


class File(Asset):
	handler = Asset.handler.adapt(default='org.contentment.file.default')
	backend = PluginReference('web.contentment.storage', default='gridfs')
	

class Search(Asset):
	query = String(default=None)
	base = Path(default='/')
	exclude = Array(String(), assign=True)
	
	handler = Asset.handler.adapt(default='org.contentment.search.default')


class Settings(Asset):
	handler = Asset.handler.adapt(default='org.contentment.settings.default')


class Theme(Asset):
	handler = Asset.handler.adapt(default='org.contentment.theme.default')
