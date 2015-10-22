# encoding: utf-8

"""A basic root controller.

Yes.  It really is just this.

There is no particular need to subclass this module, it's main use is in CMS-only application configurations.

For mix-in use, simply define the `__dispatch__` of one of your own controllers as `contentment` and you'll have
the same functionality.
"""


class ContentmentRoot:
	__slots__ = ('_ctx')
	
	__dispatch__ = 'contentment'  # This will lazy-load.
	
	def __init__(self, ctx):
		self._ctx = ctx
