# encoding: utf-8

"""

Gallery controller JSON API methods.

"""

import web.core
from web.utils.string import normalize

from web.extras.contentment.components.asset.model import Asset
from web.extras.contentment.components.file.model import File



log = __import__('logging').getLogger(__name__)
__all__ = ['GalleryMethods']



class GalleryMethods(web.core.Controller):
    def __init__(self, controller):
        self.controller = controller
    
    def bulk(self, upload):
      f = File()
      
      f.title, _, _ = upload.filename.rpartition('.')
      f.content = upload.file
      f.content.content_type = f.mimetype = upload.type
      f.content.filename = f.filename = upload.filename
      f.size = upload.length
      
      
      siblings = [i.name for i in Asset.objects(parent=self.controller.asset).only('name')]
      f.name = normalize(upload.filename.lower(), siblings)
      
      f.save()
      f.attach(self.controller.asset)
      
      return 'json:', dict()
