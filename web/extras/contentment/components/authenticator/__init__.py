# encoding: utf-8

from web.extras.contentment import release
from web.extras.contentment.api import IExtension


__all__ = ['AuthenticatorComponent', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class AuthenticatorComponent(IExtension):
    title = "Authenticator"
    summary = "Provides a basic authentication mechanism."
    description = None
    icon = 'base-authenticator'
    group = "Basic Types"
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    @property
    def model(self):
        from web.extras.contentment.components.authenticator import model
        return super(AuthenticatorComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.authenticator.controller import AuthenticatorController
        AuthenticatorController._component = self
        return AuthenticatorController
