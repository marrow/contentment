# encoding: utf-8

from web.extras.contentment import release
from web.extras.contentment.api import IComponent


__all__ = ['AssetComponent', 'controller', 'core', 'model', 'views']
log = __import__('logging').getLogger(__name__)


class AssetComponent(IComponent):
    title = "Asset"
    summary = None
    description = None
    icon = 'base-asset'
    group = "Basic Types"
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    @property
    def model(self):
        from web.extras.contentment.components.asset import model
        return super(AssetComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.asset.controller import AssetController
        AssetController._component = self
        return AssetController
    
    def authorized(self, parent):
        return False
