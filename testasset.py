# encoding: utf-8

import random

from mongoengine import ListField, IntField, EmbeddedDocumentField
from web.component.asset.model import Asset
from web.contentment.util.model import Properties


class TestAsset(Asset):
	data = ListField(IntField(), custom_data=Properties(simple=True))
	props = ListField(EmbeddedDocumentField(Properties), custom_data=Properties(simple=False))

	# __xml_exporters__ = {
	# 	'props': list_field,
	# }

	@classmethod
	def test(cls):
		return cls.objects.create(title={'en': 'Test', 'fr': 'Test'}, name='Test', tags=['one', 'another', 'third'], data=[random.randint(1, 42) for i in range(5)])


# TestAsset.__xml_exporters__.update(Asset.__xml_exporters__)
