# encoding: utf-8

"""Basic event controller."""

from web.extras.contentment.api import action, view
from web.extras.contentment.components.page.controller import PageController


log = __import__('logging').getLogger(__name__)
__all__ = ['EventController']



class EventController(PageController):
    _modify_form = "web.extras.contentment.components.event.templates.modify"
    
    @view("Event", "Display event details.")
    def view_default(self):
        return 'view', None
