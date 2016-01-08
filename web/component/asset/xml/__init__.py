# encoding: utf-8
import io
import csv
import inspect
from functools import partial
from bson.objectid import ObjectId

from mongoengine import EmbeddedDocumentField, ListField, ObjectIdField

from . importers import from_xml


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
XML_EXPORTERS_REGISTRY = {}
XML_IMPORTERS_REGISTRY = {}
ASSETS_REGISTRY = {}
__initialized = False


def get_simple_fields(record):
	for field_name in record._fields_ordered:
		field = record._fields.get(field_name)
		if field is None:
			continue
		meta = field.custom_data or {}
		if not meta.get('export', True):
			continue

		data = record._data[field_name]
		if meta.get('simple', True):
			if isinstance(field, ListField):
				output = io.StringIO()
				writer = csv.writer(output)
				writer.writerow(data)
				data = output.getvalue().strip()

			yield field_name, data


def get_complex_fields(record, level):
	for field_name in record._fields_ordered:
		field = record._fields.get(field_name)
		if field is None:
			continue
		meta = field.custom_data or {}
		if not meta.get('export', True):
			continue

		if meta.get('simple', True):
			continue

		data = record._data[field_name]
		if data is None:
			continue

		yield from process_field(data, field, field_name, record, level=level)


def process_field(data, field, field_name, record, **kwargs):
	exporter = None

	# Or get field.__xml__
	exporter = partial(field.__xml__, data) if hasattr(field, '__xml__') else None

	if exporter is None:
		# Or find XML exporter at class level
		exporter = getattr(record, '__xml_exporters__', {}).get(field_name)
		if exporter is None:
			# Or get XML exporter for this field's class
			exporter = get_xml_exporter(field)
		if exporter is not None:
			exporter = partial(exporter, record, field_name, data)

	if exporter is None and isinstance(field, EmbeddedDocumentField):
		from .templates import asset, embedded_document

		# Get __xml__ of embedded document
		if hasattr(field.document_type, '__xml__'):
			exporter = partial(field.document_type.__xml__, data)

		if exporter is None:
			# Or get XML exporter for this embedded document's class
			exporter = get_xml_exporter(field.document_type)
			if exporter is not None:
				exporter = partial(exporter, data)
			else:
				# Or use default XML exporter for documents
				exporter = partial(asset, data, level=kwargs.pop('level', 0) + 1)

		if not kwargs.get('_in_list', False):
			exporter = partial(embedded_document, record, field_name, exporter())

	if exporter is not None:
		meta = {}
		args = inspect.getargs(exporter.func.__code__).args
		if 'level' in args:
			meta['level'] = kwargs.get('level', 0)
		yield from exporter(**meta)


def __init():
	from mongoengine import ListField, ReferenceField, DateTimeField
	from web.component.asset.xml.templates import list_field, reference_field, datetime_field # circular reference
	from . import importers

	global XML_EXPORTERS_REGISTRY, XML_IMPORTERS_REGISTRY, __initialized

	XML_EXPORTERS_REGISTRY = {
		ListField: list_field,
		ReferenceField: reference_field,
		DateTimeField: datetime_field,
	}

	XML_IMPORTERS_REGISTRY = {
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

		for member in inspect.getmembers(module):
			member = member[1]

			if inspect.ismodule(member):
				if member in visited:
					continue

				visited.add(member)
				modules.append(member)

			elif inspect.isclass(member) and issubclass(member, BaseDocument) and hasattr(member, '__xml__'):
				models.add(member)

	global ASSETS_REGISTRY
	ASSETS_REGISTRY = {model.__name__: model for model in models}


def get_xml_exporter(obj):
	if not __initialized:
		__init()
	if not inspect.isclass(obj):
		obj = type(obj)
	return XML_EXPORTERS_REGISTRY.get(obj)


def get_xml_importer(obj):
	if not __initialized:
		__init()
	if not inspect.isclass(obj):
		obj = type(obj)
	return XML_IMPORTERS_REGISTRY.get(obj)


def get_asset_class(name):
	if not __initialized:
		__init()

	return ASSETS_REGISTRY.get(name)
