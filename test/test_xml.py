# encoding: utf-8

import pytest
from mongoengine import connect


from web.component.asset.model import Asset
from web.component.page.block.content import TextBlock
from web.component.page.block.reference import ReferenceBlock
from web.component.page.block.video import VideoBlock
from web.component.page.block.map import MapBlock
from web.component.career.model import Career
from web.component.page.model import Page


class TestXML:
	def test_export_import(self, tmpdir):
		from . import fixture
		from web.component.asset.xml import from_xml

		output = tmpdir.join('test.xml')
		output_f = output.open('wt')

		connection = connect('cms_test')

		root = fixture.apply()
		result1 = root.tree()

		for line in root.__xml__(True):
			output_f.write(line)
		output_f.close()

		connection.drop_database('cms_test')
		connection = connect('cms_test')

		output_f = output.open('rt')
		root = from_xml(output_f)
		output_f.close()
		result2 = root.tree()

		connection.drop_database('cms_test')

		assert result2 == result1
