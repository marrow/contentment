# encoding: utf-8

from web.extras.contentment import release
from web.extras.contentment.api import IExtension


__all__ = ['SettingsComponent', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class SettingsComponent(IExtension):
    title = "Settings"
    summary = None
    description = None
    icon = 'magic-settings'
    group = "Magic Types"
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    @property
    def model(self):
        from web.extras.contentment.components.settings import model
        return super(SettingsComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.settings.controller import SettingsController
        SettingsController._component = self
        return SettingsController
