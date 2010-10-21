# encoding: utf-8

from web.extras.contentment import release
from web.extras.contentment.api import IComponent


__all__ = ['PageComponent', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class PageComponent(IComponent):
    title = "Page"
    summary = "An embeddable page of static content."
    description = None
    icon = 'base-page'
    group = "Basic Types"
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    @property
    def model(self):
        from web.extras.contentment.components.page import model
        return super(PageComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.page.controller import PageController
        PageController._component = self
        return PageController
    
    def authorize(self, child):
        return False # TODO: Check for File instance and allow.

