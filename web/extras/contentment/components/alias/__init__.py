# encoding: utf-8

from web.extras.contentment import release
from web.extras.contentment.api import IComponent


__all__ = ['AliasComponent', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class AliasComponent(IComponent):
    title = "Alias"
    summary = "Automatically redirect to another location."
    description = None
    icon = 'base-alias'
    group = "Basic Types"
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    @property
    def model(self):
        from web.extras.contentment.components.alias import model
        return super(AliasComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.alias.controller import AliasController
        AliasController._component = self
        return AliasController
    
    def authorize(self, container, child):
        return False
