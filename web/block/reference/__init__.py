# encoding: utf-8

from mongoengine import StringField, ReferenceField

from marrow.package.loader import load

from .base import Block
from .reference_ import reference_block_list_item, render_reference_block

from web.contentment.util.model import Properties


class ReferenceBlock(Block):
	__icon__ = 'link'
	_block_list_item = reference_block_list_item
	
	# Data Definition
	
	target = ReferenceField('Asset', required=True, simple=False)
	handler = StringField(default='__embed__')
	
	def __references__(self):
		return [self.target.id if hasattr(self.target, 'id') else self.target]
	
	# Python Methods
	
	def __str__(self):
		return "Reference: " + str(self.target)
	
	def __repr__(self, extra=None):
		return super(ReferenceBlock, self).__repr__("{0.target.path}/{0.handler}".format(self,
				', ' if extra else '', extra))
	
	# Data Portability
	
	def __json__(self):
		return dict(super(ReferenceBlock, self).as_json,
				target = self._data['target'].id
			)
	
	def __html_stream__(self, context=None):
		target = self.target
		handler, _, cls = target.handler.rpartition(':')
		cls = cls.partition('.')[0]
		# print(target.handler, handler, cls, handler + ':' + cls, self.handler)
		controller = load(handler + ':' + cls)(context, target)
		result = getattr(controller, self.handler)(context)
		
		return render_reference_block(context, self, result)
	
	def __text__(self):
		return self.target.__text__()
