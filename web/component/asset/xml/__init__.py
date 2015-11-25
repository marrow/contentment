# encoding: utf-8
import io
import csv
import inspect
from functools import partial

from mongoengine import EmbeddedDocumentField, ListField

from . importers import from_xml


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
XML_EXPORTERS_REGISTRY = {}
XML_IMPORTERS_REGISTRY = {}
ASSETS_REGISTRY = {}
__initialized = False


def get_simple_fields(record):
	for field_name, field in record._fields.items():
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


def get_complex_fields(record):
	for field_name, field in record._fields.items():
		meta = field.custom_data or {}
		if not meta.get('export', True):
			continue

		data = record._data[field_name]
		if meta.get('simple', True):
			continue

		yield from process_field(data, field, field_name, record)


def process_field(data, field, field_name, record):
	exporter = None
	# Get __xml__ of embedded document
	if isinstance(field, EmbeddedDocumentField) and hasattr(field.document_type, '__xml__'):
		exporter = partial(field.document_type.__xml__, data)

	# Or get field.__xml__
	if exporter is None:
		exporter = partial(field.__xml__, data) if hasattr(field, '__xml__') else None

	if exporter is None:
		# Or find XML exporter at class level
		exporter = getattr(record, '__xml_exporters__', {}).get(field_name)
		if exporter is None:
			# Or get XML exporter for this field's class
			exporter = get_xml_exporter(field)
		if exporter is not None:
			exporter = partial(exporter, record, field_name, data)

	# Or get XML exporter for this embedded document's class
	if exporter is None and isinstance(field, EmbeddedDocumentField):
		exporter = get_xml_exporter(field.document_type)
		if exporter is not None:
			exporter = partial(exporter, data)

	if exporter is not None:
		yield from exporter()


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
