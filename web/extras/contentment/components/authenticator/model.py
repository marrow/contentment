# encoding: utf-8

import mongoengine as db

from web.extras.contentment.components.asset.model import Asset


log = __import__('logging').getLogger(__name__)
__all__ = ['Authenticator']



class Authenticator(Asset):
    default = db.StringField(default="action:authenticate", max_length=128)
    
    registering = db.BooleanField(default=False)
