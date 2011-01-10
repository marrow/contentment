# encoding: utf-8

"""Basic event controller."""

from web.extras.contentment.api import action, view
from web.extras.contentment.components.page.controller import PageController


log = __import__('logging').getLogger(__name__)
__all__ = ['AlertController']



class AlertController(PageController):
    @view("Alert", "Display alert details.")
    def view_alert(self):
        return 'view', None
