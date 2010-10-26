# encoding: utf-8

"""Basic page controller.

Textual content presentation.
"""

from web.extras.contentment.api import action, view
from web.extras.contentment.components.asset.controller import AssetController


log = __import__('logging').getLogger(__name__)
__all__ = ['PageController']



class PageController(AssetController):
    _modify_form = "web.extras.contentment.components.page.templates.modify"
    
    @view("Page", "View rendered version of this page.")
    def view_default(self):
        return 'view', None
