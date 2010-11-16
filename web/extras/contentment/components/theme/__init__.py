# encoding: utf-8

import os

from web.extras.contentment import release
from web.extras.contentment.api import ITheme


__all__ = ['ThemeComponent', 'controller', 'model']
log = __import__('logging').getLogger(__name__)


class ThemeComponent(ITheme):
    """Base theme."""
    
    title = "Theme"
    summary = "The base theme definition."
    description = None
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    @property
    def model(self):
        from web.extras.contentment.components.theme import model
        return super(ThemeComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.theme.controller import ThemeController
        ThemeController._component = self
        return ThemeController
    
    def authorized(self, container):
        return False
    
    def authorize(self, container, child):
        return False
