# encoding: utf-8

from marrow.mongo import Document
from marrow.mongo.field import Embed, String

from ..core import Block


class TextBlock(Block):
	# Legacy Representation
	content = Embed(Document, default=dict, simple=False)
	format = String(default='html', choices=['html', 'textile', 'md', 'rest'])
