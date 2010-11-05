# encoding: utf-8

import os

from web.extras.contentment import release
from web.extras.contentment.api import ITheme


__all__ = ['DefaultTheme', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class DefaultTheme(ITheme):
    """The default theme for Contentment."""
    
    title = "Default Theme"
    summary = "The default theme for Contentment."
    description = None
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    def __init__(self):
        # Determine our on-disk path for delivery of static content.
        from web.extras.contentment.themes import default
        self.path = os.path.dirname(default.__file__)
    
    @property
    def model(self):
        from web.extras.contentment.themes.default import model
        return super(DefaultTheme, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.themes.default.controller import DefaultThemeController
        DefaultThemeController._component = self
        return DefaultThemeController
    
    def authorize(self, container, child):
        return False

