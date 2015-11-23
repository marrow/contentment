# encoding: utf-8

import inspect
import cinje


XML_EXPORTERS_REGISTRY = {}

ASSETS_REGISTRY = {}

__initialized = False


def __init():
	from mongoengine import ListField, ReferenceField
	from web.component.asset.templates import list_field, reference_field # circular reference

	global XML_EXPORTERS_REGISTRY, __initialized

	XML_EXPORTERS_REGISTRY = {
		ListField: list_field,
		ReferenceField: reference_field,
	}

	__inflate_assets()
	__initialized = True


def __inflate_assets():
	import inspect
	from importlib import import_module
	from mongoengine.base import BaseDocument
	from marrow.package.canonical import name

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
	ASSETS_REGISTRY = {model.__name__: name(model) for model in models}


def get_xml_exporter(obj):
	if not __initialized:
		__init()
	if not inspect.isclass(obj):
		obj = type(obj)
	return XML_EXPORTERS_REGISTRY.get(obj)


def get_asset_class(name):
	from marrow.package.loader import load

	if not __initialized:
		__init()

	path = ASSETS_REGISTRY.get(name)
	if not path:
		return None

	return load(path)