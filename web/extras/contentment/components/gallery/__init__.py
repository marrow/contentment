# encoding: utf-8

from web.extras.contentment import release
from web.extras.contentment.api import IComponent


__all__ = ['FolderComponent', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class GalleryComponent(IComponent):
    title = "Gallery"
    summary = "An image gallery."
    description = None
    icon = 'base-gallery'
    group = "Basic Types"
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    @property
    def model(self):
        from web.extras.contentment.components.gallery import model
        return super(GalleryComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.gallery.controller import GalleryController
        GalleryController._component = self
        return GalleryController
