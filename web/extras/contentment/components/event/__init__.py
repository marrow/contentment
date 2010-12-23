# encoding: utf-8

from web.extras.contentment import release
from web.extras.contentment.api import IComponent


__all__ = ['EventComponent', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class EventComponent(IComponent):
    title = "Event"
    summary = "A scheduled event."
    description = None
    icon = 'base-event'
    group = "Basic Types"
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    @property
    def model(self):
        from web.extras.contentment.components.event import model
        return super(EventComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.event.controller import EventController
        EventController._component = self
        return EventController
    
    def authorize(self, container, child):
        from web.extras.contentment.components.file import FileComponent

        if isinstance(child, FileComponent):
            return True

        return False
