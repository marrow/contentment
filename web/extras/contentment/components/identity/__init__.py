# encoding: utf-8

from web.extras.contentment import release
from web.extras.contentment.api import IComponent


__all__ = ['IdentityComponent', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class IdentityComponent(IComponent):
    title = "Identity"
    summary = None
    description = None
    icon = 'base-identity'
    group = "Basic Types"
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    @property
    def model(self):
        from web.extras.contentment.components.identity import model
        return super(IdentityComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.identity.controller import IdentityController
        IdentityController._component = self
        return IdentityController
