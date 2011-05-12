# encoding: utf-8

import web.auth

from pytz import utc as UTC
from datetime import datetime
import mongoengine as db


class ACLRule(db.EmbeddedDocument):
    def __str__(self):
        return self.__class__.__name__


class InheritACLRules(ACLRule):
    pass


class BaseACLRule(ACLRule):
    def __str__(self):
        return self.__class__.__name__ + "(" + ("allow" if self.allow else "deny") + ", " + (self.permission if self.permission else "None") + ")"
    
    allow = db.BooleanField()
    permission = db.StringField(max_length=250)
    inheritable = db.BooleanField(default=True)
    
    def __call__(self, entity, identity, kind, name):
        kind_, _, name_ = self.permission.partition(':')
        
        if kind_ == "*":
            return self.allow
        
        if kind_ != kind:
            return None
        
        if name_ == "*":
            return self.allow
        
        if name_ != name:
            return None
        
        return self.allow


class AllUsersACLRule(BaseACLRule):
    pass


class AnonymousUsersACLRule(BaseACLRule):
    def __call__(self, entity, identity, kind, name):
        return super(AnonymousUsersACLRule, self).__call__(entity, identity, kind, name) if web.auth.anonymous else None


class AuthenticatedUsersACLRule(BaseACLRule):
    def __call__(self, entity, identity, kind, name):
        return super(AuthenticatedUsersACLRule, self).__call__(entity, identity, kind, name) if web.auth.authenticated else None


class OwnerACLRule(BaseACLRule):
    def __call__(self, entity, identity, kind, name):
        if not entity.owner or not identity:
            return None
        
        return super(OwnerACLRule, self).__call__(entity, identity, kind, name) if identity.id == entity.owner.id else None


class TargetedACLRule(BaseACLRule):
    def __str__(self):
        return "%s(%s, %s, %s%r)" % (self.__class__.__name__, "allow" if self.allow else "deny", self.permission, "not " if self.inverse else "", self.reference)
    
    inverse = db.BooleanField(default=False)
    reference = db.GenericReferenceField()


class UserACLRule(TargetedACLRule):
    def __call__(self, entity, identity, kind, name):
        if not identity:
            return False if not self.allow and self.inverse else None
        
        if not self.reference:
            return None
        
        conditional = identity.id == self.reference.id
        if self.inverse: conditional = not conditional
        
        return super(UserACLRule, self).__call__(entity, identity, kind, name) if conditional else None


class GroupACLRule(TargetedACLRule):
    def __call__(self, entity, identity, kind, name):
        conditional = self.reference not in identity.membership if self.inverse else self.reference in identity.membership
        return super(GroupACLRule, self).__call__(entity, identity, kind, name) if conditional else None


class PublicationACLRule(BaseACLRule):
    publish = db.DateTimeField(default=None)
    retract = db.DateTimeField(default=None)
    
    def __call__(self, entity, identity, kind, name):
        result = super(PublicationACLRule, self).__call__(entity, identity, kind, name)
        valid = True
        now = datetime.now(UTC)
        
        if result is None: return None
        
        if self.publish:
            valid = valid and now > self.publish
        
        if self.retract:
            valid = valid and now < self.retract
        
        if valid:
            return result
        
        return not result


class AdvancedACLRule(BaseACLRule):
    attributes = db.DictField(default=dict)
    
    def __str__(self):
        return "AdvancedACLRule(%s, %s, %r)" % ("allow" if self.allow else "deny", self.permission, self.attributes)
    
    def __call__(self, entity, identity, kind, name):
        """Disabled until further notice."""
        result = super(AdvancedACLRule, self).__call__(entity, identity, kind, name)
        
        if result is None: return None
        
        for name in self.attributes:
            if not hasattr(entity, name):
                continue
            
            value = getattr(entity, name)
            
            if value != self.attributes[name]:
                result = None
                break
        
        return result
