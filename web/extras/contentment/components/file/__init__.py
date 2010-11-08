# encoding: utf-8

import pkg_resources

from web.extras.contentment import release
from web.extras.contentment.api import IComponent

from collections import defaultdict


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
    
    def __init__(self):
        mimetypes = self.mimetypes = defaultdict(dict)
        
        for res in pkg_resources.iter_entry_points('contentment.file.format'):
            try:
                instance = res.load()()
            
            except:
                log.exception("Error scanning for file format handlers.")
                break
            
            try:
                for top, bottom in instance.mimetypes.iteritems():
                    if bottom is "*":
                        mimetypes[top] = defaultdict(lambda: instance, mimetypes[top])
                        continue
                    
                    if isinstance(bottom, list):
                        for b in bottom:
                            mimetypes[top][b] = instance
            
            except:
                log.exception("Error initializing file format handler %r.", instance)
                continue
    
    @property
    def model(self):
        from web.extras.contentment.components.file import model
        return super(FileComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.file.controller import FileController
        FileController._component = self
        return FileController
    
    def authorize(self, container, child):
        return False
