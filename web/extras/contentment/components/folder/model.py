# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""


import mongoengine as db

from web.extras.contentment.components.asset.model import Asset


log = __import__('logging').getLogger(__name__)
__all__ = ['Folder']



class Folder(Asset):
    # default = db.StringField(default="view:contents", max_length=128)
    sort = db.StringField(max_length=250) # default sort order
