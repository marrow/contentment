# encoding: utf-8

from cinje import flatten
from web.component.asset import AssetController

from .render import render_page


log = __import__('logging').getLogger(__name__)



class PageController(AssetController):
	def get(self):  # TODO: Accept matching, this is the text/html non-xhr handler.
		if __debug__:
			return flatten(render_page(self._ctx, self._doc))
		
		return render_page(self._ctx, self._doc)
	
	def __embed__(self, reference=None):
		return self._doc.__html_stream__(self._ctx)
