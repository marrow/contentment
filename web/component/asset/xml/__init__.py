# encoding: utf-8

import io
import csv
import inspect
import cinje

from inspect import getargs, getmembers, ismodule, isclass
from warnings import warn
from functools import partial
from collections import namedtuple
from bson.objectid import ObjectId
from mongoengine import EmbeddedDocumentField, ListField, ObjectIdField

from .importers import from_xml
from .templates import export_document, export_embedded_document


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
XML_EXPORTERS_REGISTRY = {}
XML_IMPORTERS_REGISTRY = {}
ASSETS_REGISTRY = {}
__initialized = False


FieldMetadata = namedtuple('FieldMetadata', ('name', 'export', 'simple'))


def collect_field_metadata(record):
	for name in record._fields_ordered:
		field = record._fields.get(name)
		
		if field is None:
			continue
		
		# Deprecated approach first.
		try:
			meta = field.custom_data
		except:
			# This is the proper way.
			export = getattr(field, 'export', True)
			simple = getattr(field, 'simple', True)
		else:  # Let someone know.
			if __debug__:  # Quiet down a bit in production environments.
				warnings.warn(
						'Deprecated use of "custom_data" field annotation on ' + field_name + ' '
						'of ' + repr(record.__class__),
						DeprecationWarning
					)
			
			# Load the values out the old way.
			export, simple = meta.get('export', True), meta.get('simple', True)
		
		return field, FieldMetadata(name, export, simple)


def get_simple_fields(record):
	for field, (name, export, simple) in collect_field_metadata(record):
		if not export or not simple:  # Potentially subtle difference here.
			continue
		
		data = record._data[name]
		
		if isinstance(field, ListField):  # CSV?  Interesting approach... --A
			output = io.StringIO()
			writer = csv.writer(output)
			writer.writerow(data)
			data = output.getvalue().strip()
		
		yield name, data


def get_complex_fields(record, level):
	for field, (name, export, simple) in collect_field_metadata(record):
		if not export or simple:  # Potentially subtle difference here.
			continue
		
		data = record._data[name]
		
		if data is None:
			continue
		
		yield from process_field(data, field, name, record, level=level)


# Check for explosions; former **kw --A
def process_field(data, field, field_name, record, level=0, _in_list=False):
	def export_consumer(exporter, *args, **kw):
		if 'level' in getargs(exporter.func.__code__).args:  # Veeeery safe... optional API.
			return exporter(*args, level=kw.get('level', level))
		else:
			return exporter(*args)
	
	def find_relevant_exporter(getter, direct, indirect=None):
		if hasattr(direct, '__xml__'):
			return export_consumer(field.__xml__, data)
		
		if indirect is not None and field_name in getattr(indirect, '__xml_exporters__', {}):
			if __debug__:
				warnings.warn(
						'Deprecated use of "__xml_exporters__" field annotation for ' + field_name + ' '
						'on ' + repr(indirect) + ', pass as "exporter=" to the field itself instead.',
						DeprecationWarning
					)
			return export_consumer(indirect.__xml_exporters__[field_name])
		
		try:  # Look up the field class in the appropriate registry.
			exporter = getter(direct)
		except (KeyError, TypeError):
			pass
		else:
			kw = {}
			args = getargs(exporter.func.__code__).args
			if 'record' in args: kw['record'] = record
			if 'field_name' in args: kw['field_name'] = field_name
			return export_consumer(exporter, data=data, **kw)  # TODO: Standardize this!
		
		raise TypeError("No exporter found.")
	
	try:
		return find_relevant_exporter(get_xml_exporter, field, record)
	except TypeError:
		pass
	
	if not isinstance(field, EmbeddedDocumentField):  # We've exhausted our options at this point.
		return []
	
	try:
		exporter = usual_culprits(get_xml_exporter, field.document_type)
	except TypeError:
		# Use the default XML exporter for documents.
		exporter = export_consumer(export_document, data, level=level + 1)
	
	if not _in_list:
		exporter = export_consumer(export_embedded_document, record, field_name, exporter())
	
	return exporter



def __init():
	from mongoengine import StringField, ListField, ReferenceField, DateTimeField
	from web.component.asset.xml.templates import list_field, reference_field, datetime_field # circular reference
	from . import importers

	global XML_EXPORTERS_REGISTRY, XML_IMPORTERS_REGISTRY, __initialized

	XML_EXPORTERS_REGISTRY = {
		ListField: list_field,
		ReferenceField: reference_field,
		DateTimeField: datetime_field,
	}

	XML_IMPORTERS_REGISTRY = {
		StringField: importers.string_field,
		ListField: importers.list_field,
		ReferenceField: importers.reference_field,
		DateTimeField: importers.datetime_field,
		ObjectIdField: lambda d, f, e: ObjectId(e),
		EmbeddedDocumentField: importers.embedded_document_field,
	}

	__inflate_assets()
	__initialized = True


def __inflate_assets():
	import inspect
	from importlib import import_module
	from mongoengine.base import BaseDocument

	models = set()
	visited = set()
	modules = ['web.component', 'web.contentment']
	modules = [import_module(module) for module in modules]

	while modules:
		module = modules.pop(0)

		for member in getmembers(module):
			member = member[1]

			if ismodule(member):
				if member in visited:
					continue

				visited.add(member)
				modules.append(member)

			elif isclass(member) and issubclass(member, BaseDocument) and hasattr(member, '__xml__'):
				models.add(member)

	global ASSETS_REGISTRY
	ASSETS_REGISTRY = {model.__name__: model for model in models}


def get_xml_exporter(obj):
	if not __initialized:
		__init()
	if not isclass(obj):
		obj = type(obj)
	return XML_EXPORTERS_REGISTRY.get(obj)


def get_xml_importer(obj):
	if not __initialized:
		__init()
	if not isclass(obj):
		obj = type(obj)
	return XML_IMPORTERS_REGISTRY.get(obj)


def get_asset_class(name):
	if not __initialized:
		__init()

	return ASSETS_REGISTRY.get(name)
