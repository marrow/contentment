# encoding: utf-8

from bson import ObjectId

from marrow.package.cache import PluginCache
from mongoengine import StringField, IntField, MapField, DateTimeField
from mongoengine import EmbeddedDocumentField, ReferenceField, ListField

from web.contentment.acl import ACLRule
from web.contentment.taxonomy import remove_children, Taxonomy, TaxonomyQuerySet
from web.contentment.util import utcnow, D_
from web.contentment.util.model import update_modified_timestamp, Properties

from .xml.templates import export_document
from .xml.templates import translated_field as export_translated_field
from .xml.importers import translated_field as import_translated_field


log = __import__('logging').getLogger(__name__)


@remove_children.signal
@update_modified_timestamp.signal
class Asset(Taxonomy):
	meta = dict(
			collection = 'asset',
			ordering = ['parent', 'order'],
			allow_inheritance = True,
			index_cls = False,
			
			indexes = [
					'path',
					('parent', 'order'),
				]
		)
	
	__icon__ = 'folder-o'
	
	# Basic Properties
	
	title = MapField(  # TODO: TranslatedField
			StringField(),
			db_field = 'a_t',  # TODO: Stop doing this.
			default = dict,
			importer = import_translated_field,
			exporter = export_translated_field,
			simple = False
		)
		
	description = MapField(  # TODO: TranslatedField
			StringField(),
			db_field = 'a_d',  # TODO: Stop doing this.
			default = dict,
			importer = import_translated_field,
			exporter = export_translated_field,
			simple = False
		)
	
	tags = ListField(
			StringField(),
			db_field='a_T',  # TODO: Stop doing this.
			default=list
		)
	
	# Magic Properties
	
	properties = EmbeddedDocumentField(
			Properties,
			db_field = 'a_p',  # TODO: Stop doing this.
			default = Properties,
			simple = False
		)
		
	acl = ListField(
			EmbeddedDocumentField(ACLRule),
			db_field = 'a_a',  # TODO: Stop doing this.
			default = list,
			simple = False
		)
	
	handler = StringField(db_field='a_h')  # TODO: PythonReferenceField('web.component') | URLPath allowing relative
	
	# Metadata
	created = DateTimeField(db_field='a_dc', default=utcnow, simple=False)
	modified = DateTimeField(db_field='a_dm', default=utcnow, simple=False)

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
	
	# Data Portability
	
	def __xml__(self, recursive=False):
		"""Return an XML representation for this Asset."""

		return export_document(self, recursive, root=True)

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
