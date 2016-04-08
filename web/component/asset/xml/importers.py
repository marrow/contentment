# encoding: utf-8
import re
import csv
from xml.etree import ElementTree
from mongoengine import ListField, EmbeddedDocument


SPACES_RE = re.compile(r'[^\S\r\n]{2,}')


def tag(element):
	data = element.tag.rsplit('}', 1)
	try:
		return data[1]
	except IndexError:
		return data[0]


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


def _from_xml(element, parent=None, parent_order=None):
	from . import get_asset_class
	from web.component.asset.xml import get_xml_importer

	cls = get_asset_class(tag(element))
	if cls is None:
		return

	if hasattr(cls, '__xml_importer__'):
		return cls.__xml_importer__(element)

	data = {}

	for field_name, value in element.attrib.items():
		field = cls._fields[field_name]
		importer = get_xml_importer(field)
		if importer is not None:
			result = importer(data, field, value)
			if result is None and field_name in data:
				continue
			data[field_name] = result
			continue

		if isinstance(field, ListField):
			data[field_name] = next(csv.reader([value]))
			continue

		data[field_name] = value

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
				field_name, field = next(((fldname, fld) for fldname, fld in cls._fields.items() if getattr(fld, 'verbose_name', None) == field_name))
			except StopIteration:
				raise exc

		if isinstance(field, ListField):
			data[field_name] = list_field(data, field, child)
			continue

		importer = getattr(cls, '__xml_importers__', {}).get(field_name) or process_field
		result = importer(data, field, child)
		
		if result is None and field_name in data:
			continue
		
		data[field_name] = result

	def save_model(cls, data):
		if issubclass(cls, EmbeddedDocument):
			obj = cls(**data)
			return obj
		
		obj = cls(**data)

		if parent:
			if not obj.path:
				obj.path = parent.path.rstrip('/') + '/' + obj.name
		
			obj.parent = parent
			obj.parents = (parent.parents or []) + [parent.to_dbref()]
			# Evaluate obj.parents so it will be saved as dbrefs.
			obj.parents
			obj.order = parent_order
		
		if obj.id:
			identifier = obj.id
			obj_data = obj.to_mongo()
			del obj_data[obj._fields[obj._meta['id_field']].db_field]
			
			cls._get_collection().update({'_id': identifier}, {'$set': obj_data}, upsert=True)
			
			return cls.objects.get(id=identifier)
		
		obj.save()
		return obj
		
	parent_obj = save_model(cls, data)
	
	for i, child in enumerate(children):
		_from_xml(child, parent=parent_obj, parent_order=i)
	
	return parent_obj


def process_field(data, field, element):
	from web.component.asset.xml import get_xml_importer

	importer = get_xml_importer(field)
	if importer is not None:
		return importer(data, field, element)


def string_field(data, field, element):
	return element.text if hasattr(element, 'text') else element


def list_field(data, field, element):
	return [process_field(data, field.field, child) for child in element]


def reference_field(data, field, element):
	from bson import DBRef
	from web.component.asset.model import Asset
	
	identifier = element.get('id')
	
	if not identifier:
		return Asset.objects.only('id').get(path=element.get('path')).to_dbref()
	
	return DBRef(collection=element.get('collection'), id=element.get('id'))


def map_field(data, field, element):
	from web.component.asset.xml import get_xml_importer
	
	key = next(iter(element.attrib.values()))
	
	importer = get_xml_importer(field.field)
	if importer is not None:
		data.setdefault(tag(element), {})[key] = importer(data, field.field, element)
		return
	
	data.setdefault(tag(element), {})[key] = element.text


def text_block_content(data, field, element):
	element.text = re.sub(SPACES_RE, ' ', element.text)
	map_field(data, field, element)


def datetime_field(data, field, element):
	from datetime import datetime
	from . import DATETIME_FORMAT
	return datetime.strptime(element.get('at').strip(), DATETIME_FORMAT)


def embedded_document_field(data, field, element):
	if tag(element) in field.document_type._subclasses:
		obj = _from_xml(element)
	else:
		data = {}
		for sub in element:
			sub = _from_xml(sub)
			data.update(sub._data)
		obj = field.document_type(**data) if data else None
	return obj
