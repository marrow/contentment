# encoding: utf-8

log = __import__('logging').getLogger(__name__)


class ContentmentRoot:
	__slots__ = ('_ctx')
	
	__dispatch__ = 'contentment'  # This will lazy-load.
	
	def __init__(self, ctx):
		self._ctx = ctx
