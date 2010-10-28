# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""

import hashlib

import mongoengine as db

from hashlib import sha512

from web.extras.contentment.components.asset.model import Asset

from marrow.util.bunch import Bunch


log = __import__('logging').getLogger(__name__)
__all__ = ['Credential', 'PasswordCredential', 'Identity']



class Credential(db.EmbeddedDocument):
    kind = db.StringField(max_length=48)
    identity = db.StringField(max_length=250, unique=True)
    value = db.StringField(max_length=250)
    metadata = db.DictField(default={})


class PasswordCredential(Credential):
    kind = db.StringField(max_length=48, default="password")
    
    def _set_password(self, value):
        self.value = sha512(value).hexdigest()
    
    password = property(lambda self: self.value, _set_password)


class Identity(Asset):
    meta = dict(indexes=[('credentials.kind', 'credentials.identity')])
    
    # default = db.StringField(default="view:contents", max_length=128)
    
    email = db.StringField(max_length=250, required=True)
    
    credentials = db.ListField(db.EmbeddedDocumentField(PasswordCredential), default=[])
    
    membership = db.ListField(db.GenericReferenceField(), default=[])
    permissions = db.ListField(db.StringField(max_length=250), default=[])
    
    @classmethod
    def lookup(cls, identifier):
        uid, credential = identifier
        
        user = cls.objects.with_id(uid)
        
        if not user:
            return None
        
        cred = None
        
        for i in user.credentials:
            if i.identity == credential:
                cred = i
                break
        
        bundle = Bunch(identity=user, credential=cred)
        bundle.effective = [i for i in user.permissions]
        
        for cred in user.credentials:
            if cred.identity == identifier:
                for perm in cred.permissions:
                    if perm.startswith('-'):
                        bundle.effective.remove(perm[1:])
                        break
                    bundle.effective.append(perm)
                break
        
        bundle.permissions = set(bundle.effective)
        
        return bundle
    
    @classmethod
    def authenticate(cls, identifier, secret):
        password_hash = hashlib.sha512(secret).hexdigest()
        del secret
        
        user = cls.objects(
                credentials__kind = 'password',
                credentials__identity = identifier,
                credentials__value = password_hash
            ).only('id').first()
        
        if not user: return None
        _id = user.id
        
        return (_id, identifier), cls.lookup((_id, identifier))
    
