# encoding: utf-8

"""Basic page controller.

Textual content presentation.
"""

from web.extras.contentment.api import action, view
from web.extras.contentment.components.asset.controller import AssetController

from web.extras.contentment.components.page.core import PageMethods


log = __import__('logging').getLogger(__name__)
__all__ = ['PageController']



class PageController(AssetController):
    def __init__(self, *args, **kw):
        super(PageController, self).__init__(*args, **kw)
        
        self.api_page = PageMethods(self)
    
    @view("Page", "View rendered version of this page.")
    def view_page(self):
        return 'view', None
