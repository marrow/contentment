# encoding: utf-8

""""""


import mongoengine as db

from web.extras.contentment.components.folder.model import Folder


log = __import__('logging').getLogger(__name__)
__all__ = ['Gallery']



class Gallery(Folder):
    default = db.StringField(default="view:thumbnails", max_length=128)
    
