# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""


import mongoengine as db

from hashlib import sha512

from web.extras.contentment.components.asset.model import Asset


log = __import__('logging').getLogger(__name__)
__all__ = ['Credential', 'PasswordCredential', 'Identity']
__model__ = __all__



class Credential(db.EmbeddedDocument):
    kind = db.StringField(max_length=48)
    identity = db.StringField(max_length=250, unique=True)
    value = db.StringField(max_length=250)
    metadata = db.DictField(default={})


class PasswordCredential(Credential):
    kind = db.StringField(max_length=48, default="password")
    __value = db.StringField('value', max_length=250)
    
    def _set_value(self, value):
        self.__value = sha512(value).hexdigest()
    
    value = property(lambda self: self.__value, _set_value)


class Identity(Asset):
    meta = dict(
            indexes=[('credentials.kind', 'credentials.identity')]
        )
    
    email = db.StringField(max_length=250, required=True, unique=True)
    
    credentials = db.ListField(db.EmbeddedDocumentField(Credential), default=[])
    
    membership = db.ListField(db.GenericReferenceField(), default=[])
