# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""


import mongoengine as db

from web.extras.contentment.components.asset.model import Asset


log = __import__('logging').getLogger(__name__)
__all__ = ['Folder']
__model__ = __all__



class Folder(Asset):
    sort = db.StringField(max_length=250)
