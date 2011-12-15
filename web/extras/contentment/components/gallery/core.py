# encoding: utf-8

"""

Gallery controller JSON API methods.

"""

import web.core

from web.extras.contentment.components.file.model import File



log = __import__('logging').getLogger(__name__)
__all__ = ['GalleryMethods']



class GalleryMethods(web.core.Controller):
    def __init__(self, controller):
        self.controller = controller
    
    def bulk(self, upload):
      f = File()
      
      f.title, _, _ = upload.filename.rpartition('.')
      f.name = upload.filename
      f.content = upload.file
      f.content.content_type, f.mimetype = upload.type
      f.content.filename, f.filename = upload.filename
      f.size = upload.length
      
      return 'json:', dict()
