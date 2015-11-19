# encoding: utf-8

from functools import partial

from mongoengine import EmbeddedDocumentField, ListField


XML_EXCLUDE = ('parent', 'parents', 'children')


def get_simple_fields(record):
	for field_name, field in record._fields.items():
		if field_name in XML_EXCLUDE:
			continue

		meta = field.custom_data or {}
		if not meta.get('export', True):
			return

		data = record._data[field_name]
		if meta.get('simple', True):
			yield field_name, data


def get_complex_fields(record):
	for field_name, field in record._fields.items():
		if field_name in XML_EXCLUDE:
			continue

		meta = field.custom_data or {}
		if not meta.get('export', True):
			continue

		data = record._data[field_name]
		if meta.get('simple', True):
			continue

		yield from process_field(data, field, field_name, record)


def process_field(data, field, field_name, record):
	exporter = None
	if isinstance(field, EmbeddedDocumentField) and hasattr(field.document_type, '__xml__'):
		exporter = partial(field.document_type.__xml__, data)
	if exporter is None:
		exporter = partial(field.__xml__, data) if hasattr(field, '__xml__') else None
	if exporter is None:
		exporter = getattr(record, '__xml_handlers__', {}).get(field_name)
		if exporter is not None:
			exporter = partial(exporter, record, field_name, data)
	if exporter is not None:
		yield from exporter()