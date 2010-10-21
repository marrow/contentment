# encoding: utf-8

from web.extras.contentment import release
from web.extras.contentment.api import IComponent


__all__ = ['FileComponent', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class FileComponent(IComponent):
    title = "File"
    summary = "Generic file upload."
    description = None
    icon = 'base-file'
    group = "Basic Types"
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    @property
    def model(self):
        from web.extras.contentment.components.file import model
        return super(FileComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.file.controller import FileController
        FileController._component = self
        return FileController
