# encoding: utf-8

from functools import partial

from mongoengine import EmbeddedDocumentField
from .xml_exporters import get_xml_exporter


def get_simple_fields(record):
	for field_name, field in record._fields.items():
		meta = field.custom_data or {}
		if not meta.get('export', True):
			continue

		data = record._data[field_name]
		if meta.get('simple', True):
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
		exporter = getattr(record, '__xml_handlers__', {}).get(field_name)
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