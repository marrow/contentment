# encoding: utf-8

""""""


import mongoengine as db

from web.extras.contentment.components.folder.model import Folder


log = __import__('logging').getLogger(__name__)
__all__ = ['Gallery']



class ScaleSettings(db.EmbeddedDocument):
    xy = db.IntField(default=None)
    x = db.IntField(default=None)
    y = db.IntField(default=None)
    square = db.BooleanField(default=False)
    
    reflect = db.BooleanField(default=False)
    amount = db.FloatField(default=0.75)
    opacity = db.FloatField(default=0.4)


class Gallery(Folder):
    default = db.StringField(default="view:thumbnails", max_length=128)
    
    thumbnail = db.EmbeddedDocumentField(ScaleSettings, default=lambda: ScaleSettings(xy=96, square=True))
    polaroid = db.EmbeddedDocumentField(ScaleSettings, default=lambda: ScaleSettings(xy=175, square=True))
    lightbox = db.EmbeddedDocumentField(ScaleSettings, default=lambda: ScaleSettings(x=960, y=600))
    slideshow = db.EmbeddedDocumentField(ScaleSettings, default=lambda: ScaleSettings(x=960, y=600))
    flow = db.EmbeddedDocumentField(ScaleSettings, default=lambda: ScaleSettings(y=270, reflect=True))
