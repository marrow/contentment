# encoding: utf-8

import os

from web.extras.contentment import release


__all__ = ['DefaultTheme', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class DefaultTheme(object):
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
    def enabled(self):
        return True
    
    @property
    def model(self):
        from web.extras.contentment.components.asset.model import Asset
        from web.extras.contentment.themes.default import model
        
        models = dict([(i, getattr(model, i)) for i in model.__model__])
        
        for i, j in models.iteritems():
            if issubclass(j, Asset):
                j._component = self
                
                if not getattr(j, 'controller', None):
                    # We allow overriding of this.
                    j.controller = property(lambda self: self._component.controller(self))
        
        return models
    
    @property
    def controller(self):
        from web.extras.contentment.themes.default.controller import DefaultThemeController
        DefaultThemeController._component = self
        return DefaultThemeController
    
    def constructor(self, **kw):
        """A factory method to create new instances of this component."""
        from web.extras.contentment.themes.default.model import DefaultTheme
        return DefaultTheme(**kw)
    
    def authorize(self, child):
        return False

