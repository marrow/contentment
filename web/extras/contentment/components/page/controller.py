# encoding: utf-8

"""Basic page controller.

Textual content presentation.
"""

from web.extras.contentment.components.asset.controller import AssetController


log = __import__('logging').getLogger(__name__)
__all__ = ['PageController']



class PageController(AssetController):
    """"""
    
    def view_default(self):
        return self._template('view', base='.'.join(PageController.__module__.split('.')[:-1]))
