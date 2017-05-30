# encoding: utf-8

from cinje import interruptable
from marrow.mongo.document import Block
from marrow.mongo.field import Array, Embed


log = __import__('logging').getLogger(__name__)


class Page(Asset):
	"""An asset containing user-editable rich content organized into logical blocks.
	
	Blocks are stored external to the Page resource itself.
	"""
	
	Block = Block
	
	# Field Definitions
	
	related = Array(Reference(Asset), assign=True)
	template = Reference(Asset, default=None)
	style = Embed('Style', assign=True)
	handler = Asset.handler.adapt(default='page.default')
	
	# Legacy Field Definitions
	
	content = Array(Embed(Block), assign=True)
	
	# Query Methods
	
	def find_blocks(self, *args, **kw):
		"""Find blocks associated with this Page."""
		
		return self.Block.blocks_for(self, kw.pop('lang'))
	
	# Self-Rendering Protocols
	
	def __embed__(self, context):
		container = self.style.container
		
		if container:  # Given a wrapping container template, stream the prefix.
			kw = dict(self.style.attributes) if self.style.attributes else {}
			kw.setdefault('id', str(self.id))
			container = container(context, **kw)
			
			yield from interruptable(container)
		
		for block in self.blocks:
			yield from block.__embed__(context)
		
		if container:  # Yield the remainder (postfix) of the wrapping template.
			yield from container
	
	# Useful for rapidly loading assets that would be lazily loaded later anyway.
	# For example, during page rendering, or during page export to a static mirror.
	
	def __references__(self):
		"""Identify the references to all assets required for rendering this page."""
		
		# First, we identify the Block subclasses that might reference another Asset.
		participants = tuple(j for j in (get_document(i) for i in Block._subclasses) if hasattr(j, '__references__'))
		
		content = self.__class__.objects.no_dereference().scalar('content').get(id=self.id)
		
		for chunk in content:
			if not isinstance(chunk, participants):
				continue
			
			for reference in chunk.__references__():
				yield reference
	
	# Data Portability
	
	def __json__(self):
		return dict(super().__json__(), 
				contents = [i.as_json for i in self.content]  # Capture child nodes.
			)
