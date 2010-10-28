# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""


import mongoengine as db

from web.extras.contentment.components.asset.model import Asset


log = __import__('logging').getLogger(__name__)
__all__ = ['File']



class File(Asset):
    default = db.StringField(default="view:preview", max_length=128)
    content = db.FileField()
