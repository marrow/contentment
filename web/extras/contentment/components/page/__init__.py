# encoding: utf-8

import pkg_resources

from web.extras.contentment import release
from web.extras.contentment.api import IComponent

from marrow.util.bunch import Bunch


__all__ = ['PageComponent', 'controller', 'model', 'templates', 'engines']
log = __import__('logging').getLogger(__name__)

engines = Bunch()


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
    
    def authorize(self, container, child):
        from web.extras.contentment.components.file import FileComponent
        
        if isinstance(child, FileComponent):
            return True
        
        return False


for res in pkg_resources.iter_entry_points('contentment.renderer'):
    try:
        instance = res.load()
    
    except:
        log.exception("Error scanning page renderers.")
        raise
    
    try:
        if hasattr(instance, '__call__'):
            instance = instance()
        
        engines[res.name] = instance
    
    except:
        log.exception("Error initializing page renderer %r.", instance)
        continue

log.info("Loaded page renderers: %s", ', '.join([i.__class__.__name__ for i in engines.itervalues()]))
