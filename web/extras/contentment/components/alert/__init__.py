# encoding: utf-8

from web.extras.contentment import release
from web.extras.contentment.api import IComponent


__all__ = ['AlertComponent', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class AlertComponent(IComponent):
    title = "Alert"
    summary = "A high-priority short message."
    description = None
    icon = 'base-alert'
    group = "Basic Types"
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    @property
    def model(self):
        from web.extras.contentment.components.alert import model
        return super(AlertComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.alert.controller import AlertController
        AlertController._component = self
        return AlertController
    
    def authorize(self, container, child):
        from web.extras.contentment.components.alias import AliasComponent
        from web.extras.contentment.components.file import FileComponent

        return isinstance(child, (AliasComponent, FileComponent))
