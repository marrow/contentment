# encoding: utf-8

from web.extras.contentment import release
from web.extras.contentment.api import IComponent


__all__ = ['SearchComponent', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class SearchComponent(IComponent):
    title = "Search"
    summary = "Site-wide search and saved searches."
    description = None
    icon = 'base-search'
    group = "Basic Types"
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    @property
    def model(self):
        from web.extras.contentment.components.search import model
        return super(SearchComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.search.controller import SearchController
        SearchController._component = self
        return SearchController
    
    def authorize(self, container, child):
        return False
