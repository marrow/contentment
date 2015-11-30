# encoding: utf-8
import re
import csv
from xml.etree import ElementTree
from mongoengine.base import BaseDocument
from mongoengine import ListField, EmbeddedDocumentField, EmbeddedDocument


SPACES_RE = re.compile(r'[^\S\r\n]{2,}')


def tag(element):
	return element.tag.rsplit('}', 1)[1]


def from_xml(data):
	element = None
	if hasattr(data, 'read') and callable(data.read):
		element = ElementTree.fromstring(data.read())[0]

	if isinstance(data, str):
		try:
			with open(data, 'rt') as file:
				element = ElementTree.parse(file).getroot()[0]
		except FileNotFoundError:
			element = ElementTree.fromstring(data)

	if element is None:
		raise ValueError("data must be file-like object, file path string or XML string.")

	return _from_xml(element)


def _from_xml(element):
	from . import get_asset_class

	cls = get_asset_class(tag(element))
	if cls is None:
		return

	if hasattr(cls, '__xml_importer__'):
		return cls.__xml_importer__(element)

	data = dict(element.attrib)
	for field_name, value in data.items():
		if isinstance(cls._fields[field_name], ListField):
			data[field_name] = next(csv.reader([value]))

	children = []

	for child in element:
		child_cls = get_asset_class(tag(child))
		if child_cls is not None:
			children.append(child)
			continue

		field_name = tag(child)
		try:
			field = cls._fields[field_name]
		except KeyError as exc:
			try:
				field_name, field = next(((fldname, fld) for fldname, fld in cls._fields.items() if fld.verbose_name == field_name))
			except StopIteration:
				raise exc

		if isinstance(field, ListField):
			data[field_name] = list_field(data, field, child)
			continue

		if isinstance(field, EmbeddedDocumentField):
			importer = getattr(field.document_type, '__xml_importer__', lambda: None)
			result = importer(child)
		else:
			importer = getattr(cls, '__xml_importers__', {}).get(field_name) or process_field
			result = importer(data, field, child)

		if result is None and field_name in data:
			continue

		if field_name in data:
			if isinstance(result, BaseDocument):
				data[field_name]._data.update(result._data)
				continue

		data[field_name] = result

	def save_model(obj):
		obj.__class__.objects(id=obj.id).update_one(upsert=True, **obj._data)

	result_obj = cls(**data)
	if not isinstance(result_obj, EmbeddedDocument):
		save_model(result_obj)

	for child in children:
		child_obj = _from_xml(child)
		print(child_obj)
		child_obj.parent = result_obj
		if not isinstance(child_obj, EmbeddedDocument):
			save_model(child_obj)

	return result_obj


def process_field(data, field, element):
	from web.component.asset.xml import get_xml_importer

	if isinstance(field, EmbeddedDocumentField):
		content = _from_xml(element)
		return content

	importer = get_xml_importer(field)
	if importer is not None:
		return importer(data, field, element)


def list_field(data, field, element):
	return [process_field(data, field.field, child) for child in element]


def reference_field(data, field, element):
	from bson import DBRef
	return DBRef(collection=element.get('collection'), id=element.get('id'))


def translated_field(data, field, element):
	data.setdefault(tag(element), {})[next(iter(element.attrib.values()))] = element.text


def text_block_content(data, field, element):
	element.text = re.sub(SPACES_RE, ' ', element.text)
	translated_field(data, field, element)


def datetime_field(data, field, element):
	from datetime import datetime
	from . import DATETIME_FORMAT
	return datetime.strptime(element.get('at').strip(), DATETIME_FORMAT)
