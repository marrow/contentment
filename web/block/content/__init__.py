# encoding: utf-8

from mongoengine import StringField, MapField, URLField, ImageField

from web.contentment.util import D_

from .base import Block
from .content_ import render_text_block

from web.component.asset.xml.templates import text_block_content
from web.component.asset.xml.importers import text_block_content as text_block_content_importer
from web.contentment.util.model import Properties


class DescriptionBlock(Block):
	__icon__ = 'asterisk'


class TextBlock(Block):
	__icon__ = 'font'

	__xml_exporters__ = {
		'content': text_block_content,
	}

	__xml_importers__ = {
		'content': text_block_content_importer,
	}
	
	content = MapField(StringField(), default=dict, simple=False)  # TODO: TranslatedField.
	format = StringField(default='html', choices=['html', 'textile', 'md', 'rest'])  # TODO: Dynamic.
	
	# Data Portability
	
	def __html_stream__(self, context=None):
		return render_text_block(context, self, D_(self.content))
	
	def __json__(self):
		return dict(super(TextBlock, self).as_json,
				target = self._data['target'].id
			)
	
	def __text__(self):
		return ''  # TODO: Content extraction.


class QuoteBlock(Block):
	__icon__ = 'wc-b-quote'
	
	pass


class ButtonBlock(Block):
	__icon__ = 'wc-b-button'
	
	label = MapField(StringField(), db_field='c', default=dict)  # TODO: TranslatedField.
	target = URLField(db_field='t')


class ImageBlock(Block):
	__icon__ = 'wc-b-image'
	
	image = ImageField(db_field='i')
	source = URLField(db_field='s')
	target = URLField(db_field='t')
	caption = MapField(StringField(), db_field='c', default=dict)  # TODO: TranslatedField.
