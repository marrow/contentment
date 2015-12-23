# encoding: utf-8

from bson import ObjectId

from marrow.package.cache import PluginCache
from mongoengine import Document
from mongoengine import EmbeddedDocumentField
from mongoengine import StringField, IntField, MapField, DateTimeField, ReferenceField, CachedReferenceField, ListField

from web.contentment.acl import ACLRule
from web.contentment.taxonomy import remove_children, TaxonomyQuerySet, Taxonomy
from web.contentment.util import utcnow, D_
from web.contentment.util.model import update_modified_timestamp, Properties as P
#from web.contentment.okapi import update_full_text_index, remove_full_text_index, Indexed
from web.component.asset.xml import templates, importers

log = __import__('logging').getLogger(__name__)


#@update_full_text_index.signal
#@remove_full_text_index.signal
@remove_children.signal
@update_modified_timestamp.signal
class Asset(Taxonomy):
	meta = dict(
			collection = 'asset',
			ordering = ['order'],
			allow_inheritance = True,
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

	# Basic Properties
	title = MapField(StringField(), db_field='a_t', default=dict, export=True, simple=False)  # TODO: TranslatedField
	description = MapField(StringField(), db_field='a_d', default=dict, export=True, simple=False)  # TODO: TranslatedField
	tags = ListField(StringField(), db_field='a_T', default=list, export=True, simple=True)
	
	# Magic Properties
	properties = EmbeddedDocumentField(P, db_field='a_p', default=P, export=True, simple=False)
	acl = ListField(EmbeddedDocumentField(ACLRule), db_field='a_a', default=list, export=True, simple=False)
	handler = StringField(db_field='a_h', export=True, simple=True)  # TODO: PythonReferenceField('web.component') | URLPath allowing relative
	
	# Metadata
	created = DateTimeField(db_field='a_dc', default=utcnow, export=True, simple=False)
	modified = DateTimeField(db_field='a_dm', default=utcnow, export=True, simple=False)

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
