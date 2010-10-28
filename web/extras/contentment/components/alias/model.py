# encoding: utf-8

import mongoengine as db

from web.extras.contentment.components.asset.model import Asset


log = __import__('logging').getLogger(__name__)
__all__ = ['Alias']



class Alias(Asset):
    default = db.StringField(default="view:redirect", max_length=128)
    
    target = db.StringField()
    
    hits = db.IntField(min_value=0, default=0)
    detailed = db.BooleanField(default=True)
    unique = db.BooleanField(default=False) # track only unique visitors
    session = db.BooleanField(default=False) # register this alias in the session for tracking
