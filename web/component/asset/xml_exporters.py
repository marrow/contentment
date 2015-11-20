# encoding: utf-8

import inspect

from .templates import list_field, reference_field


XML_EXPORTERS_REGISTRY = {}

__initialized = False


def __init():
	from mongoengine import ListField, ReferenceField

	global XML_EXPORTERS_REGISTRY, __initialized

	XML_EXPORTERS_REGISTRY = {
		ListField: list_field,
		ReferenceField: reference_field,
	}
	__initialized = True


def get_xml_exporter(obj):
	if not __initialized:
		__init()
	if not inspect.isclass(obj):
		obj = type(obj)
	return XML_EXPORTERS_REGISTRY.get(obj)
