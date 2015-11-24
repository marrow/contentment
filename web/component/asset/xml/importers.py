# encoding: utf-8
import csv
from mongoengine import ListField, EmbeddedDocumentField

from web.contentment.util.model import Properties


def tag(element):
	return element.tag.rsplit('}', 1)[1]


def process_instance(element):
	from . import get_asset_class

	cls = get_asset_class(tag(element))
	if cls is Properties:
		return
	if cls is None:
		return

	if hasattr(cls, '__xml_importer__'):
		return cls.__xml_importer__(element)

	data = dict(element.attrib)
	for field_name, value in data.items():
		if isinstance(cls._fields[field_name], ListField):
			data[field_name] = next(csv.reader([value]))

	for child in element:
		child_cls = get_asset_class(tag(child))
		if child_cls is not None:
			process_instance(child)
			continue

		field_name = tag(child)
		try:
			field = cls._fields[field_name]
		except KeyError:
			continue
		if isinstance(field, ListField):
			data[field_name] = []
			list_field(data, field, child)
			continue

		importer = getattr(cls, '__xml_importers__', {}).get(field_name)
		if importer is None:
			importer = process_field

		result = importer(data, field, child)
		if result is None:
			if field_name in data:
				continue

		data[field_name] = result

	return cls(**data)


def process_field(data, field, element):
	from web.component.asset.xml import get_xml_importer

	if isinstance(field, EmbeddedDocumentField):
		content = process_instance(element)
		return content

	field_name = tag(element)
	importer = get_xml_importer(field_name)
	if importer is not None:
		return importer(data, field, element)


def list_field(data, field, element):
	return [process_field(data, field.field, child) for child in element]


def reference_field(data, field, element):
	from bson import DBRef
	return DBRef(collection=element.get('collection'), id=element.get('id'))


def translated_field(data, field, element):
	data.setdefault(tag(element), {})[next(iter(element.attrib.values()))] = element.text


def datetime_field(data, field, element):
	from datetime import datetime
	from . import DATETIME_FORMAT
	return datetime.strptime(element.text.strip(), DATETIME_FORMAT)
