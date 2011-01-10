# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""

import hashlib

import mongoengine as db

from hashlib import sha512

import web.core

from web.extras.contentment.components.asset.model import Asset

from marrow.util.bunch import Bunch

from yubico import yubico
from yubico import yubico_exceptions


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


class YubikeyCredential(Credential):
    kind = db.StringField(max_length=48, default="yubikey")



class Identity(Asset):
    meta = dict(indexes=[('credentials.kind', 'credentials.identity')])
    
    # default = db.StringField(default="view:contents", max_length=128)
    
    email = db.StringField(max_length=250, required=True)
    
    credentials = db.ListField(db.EmbeddedDocumentField(Credential), default=[])
    
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
        use_pw, use_yk = secret[0] != '', secret[1] != ''
        password_hash, yubikey = hashlib.sha512(secret[0]).hexdigest(), secret[1]
        del secret
        
        users = []
        
        if use_pw:
            log.debug("Validating password credential.")
            users.append(cls.objects(
                    credentials__kind = 'password',
                    credentials__identity = identifier,
                    credentials__value = password_hash
                ).only('id').first())
        
        if use_yk:
            log.debug("Validating Yubikey credential.")
            client = yubico.Yubico(
                    web.core.config['web.auth.yubikey.client'],
                    web.core.config['web.auth.yubikey.key'],
                    True if web.core.config['web.auth.yubikey.secure'] == 'True' else False
                )
            
            try:
                status = client.verify(yubikey, return_response=True)
                log.debug("Yubikey response: %r", status)
            
            except:
                log.exception("Error validating Yubikey.")
                return None
            
            if not status:
                log.warn("Invalid Yubikey response: %r", status)
                return None
            
            log.debug("Searching for yubikey identity with identifier %r and value %r.", identifier, yubikey[:12])
            
            users.append(cls.objects(
                    credentials__kind = 'yubikey',
                    credentials__identity = identifier,
                    credentials__value = yubikey[:12]
                ).only('id').first())
        
        users = [i for i in users if i is not None]
        
        log.debug("Retrieved users: %r", [i.id for i in users])
        
        if not users:
            log.warn("No credentials found.")
            return None
        
        if len(users) > 1:
            log.warn("Multiple credentials found; all must validate to same user.")
            against = users[0]
            for i in users:
                if i.id != against.id:
                    log.warn("One of the identities does not validate.")
                    return None
        
        user = users[0]
        
        log.debug("Authenticated as user ID %r.", user.id)
        
        if not user: return None
        _id = user.id
        
        return (_id, identifier), cls.lookup((_id, identifier))
    
