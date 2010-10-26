# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""

import re

from datetime import datetime

import mongoengine as db


log = __import__('logging').getLogger(__name__)
__all__ = [
        'Asset', 'ChangeSet', 'ACLRule',
        'InheritACLRules', 'BaseACLRule', 'TargetedACLRule',
        'AllUsersACLRule',
        'AnonymousUsersACLRule',
        'AuthenticatedUsersACLRule',
        'OwnerACLRule',
        'UserACLRule',
        'GroupACLRule',
        'AdvancedACLRule'
    ]



class ACLRule(db.EmbeddedDocument):
    pass

class InheritACLRules(ACLRule):
    pass

class BaseACLRule(ACLRule):
    allow = db.BooleanField()
    permission = db.StringField(max_length=250)
    inheritable = db.BooleanField(default=True)

class AllUsersACLRule(BaseACLRule):
    pass

class AnonymousUsersACLRule(BaseACLRule):
    pass

class AuthenticatedUsersACLRule(BaseACLRule):
    pass

class OwnerACLRule(BaseACLRule):
    pass

class TargetedACLRule(BaseACLRule):
    reference = db.GenericReferenceField()

class UserACLRule(TargetedACLRule):
    pass

class GroupACLRule(TargetedACLRule):
    pass

class AdvancedACLRule(BaseACLRule):
    attributes = db.DictField(default=dict)


class Asset(db.Document):
    meta = dict(
            collection="assets",
            ordering=['parents', 'name'],
            indexes=[('parents', 'name'), 'parent', 'name', 'path', 'owner', 'created', 'modified']
        )
    
    _component = None
    controller = None
    
    id = db.ObjectIdField('_id')
    
    # Relationship information.
    parent = db.GenericReferenceField(default=None)
    parents = db.ListField(db.GenericReferenceField(), default=list)
    children = db.ListField(db.GenericReferenceField(), default=list)
    path = db.StringField(default="/")
    
    # Basic properties.
    name = db.StringField(max_length=250, required=True) # unique_with="parent"
    title = db.StringField(max_length=250, required=True)
    description = db.StringField()
    
    # Magic properties.
    immutable = db.BooleanField(default=False)
    default = db.StringField(default="view:default", max_length=128)
    tags = db.ListField(db.StringField(max_length=32), default=list)
    properties = db.DictField(default=dict)
    acl = db.ListField(db.EmbeddedDocumentField(ACLRule), default=list)
    
    # Ownership and dates.
    owner = db.GenericReferenceField()
    created = db.DateTimeField(default=datetime.utcnow)
    modified = db.DateTimeField()
    
    @property
    def acl_(self):
        """Determine the canonical ACL for the current Asset instance.
        
        The method:
        
            1. Load the ACLs (just the ACLs) for all nodes from the current node to the root.
            2. Separate the root ACL (it's special).
            3. Iterate through the root ACL until hitting the 'inherit' node.
            4. Iterate through the ACL for the current node.
            5. If the current node inherits, change the current node to be its parent and repeat #4.
            6. If we run out, continue processing the root ACL's final entries.
        
        The first ACL rule to return True or False wins.
        """
        
        nodes = self.parents + [self]
        root = nodes.pop(0)
        
        current = self
        
        
        
        while True:
            for rule in current.acl.rules:
                if current is self or rule.inheritable:
                    yield current, rule
            
            if not current.parent:
                break
            
            current = current.parent
    
    def attach(self, parent):
        if self.parent:
            self.parent.children.remove(self)
            self.parent.save()
        
        self.parent = parent
        self.parents = (parent.parents if parent.parents else []) + [parent]
        
        self.path = '/' + '/'.join([i.name for i in self.parents][1:] + [self.name])
        
        self.save()
        
        if not parent.children:
            parent.children = []
        
        parent.children.append(self)
        parent.save()
        
        nodes = list(self.children)
        
        while nodes:
            node = nodes.pop()
            
            node.parents = (node.parent.parents if node.parent.parents else []) + [node.parent]
            node.path = '/' + '/'.join([i.name for i in node.parents] + [node.name])
            
            if node.children:
                nodes.extend(node.children)
            
            node.save()
    
    def delete(self, safe=False):
        # Depth-first cascading delete.
        for i in self.children:
            i.delete()
        
        # Remove reference to self from parent asset.
        if self.parent:
            self.parent.children.remove(self)
            self.parent.save()
        
        # Actually delete this asset.
        return super(Asset, self).delete(safe=safe)
    
    @property
    def descendants(self):
        """Return all descendants of this asset."""
        pass


class ChangeSet(db.Document):
    meta = dict(
            collection="changesets",
            ordering=['asset', 'date'],
            indexes=[('asset', 'date')]
        )
    
    id = db.ObjectIdField('_id')
    
    asset = db.ReferenceField(Asset)
    date = db.DateTimeField(default=datetime.utcnow)
    changes = db.DictField(default=dict)


'''
class ProperyInheritance(object):
    """A dictionary (associative array) that retreives the Property for a given asset.
    
    This differs from the _properties association proxy in that it will inherit properties from parent assets."""
    
    def __init__(self, asset):
        """We'll need to know the asset we are returning properties for later."""
        
        self.asset = asset
    
    def __repr__(self):
        """Return a string representation of a PropertyInheritance instance."""
        
        return "PropertyInheritance(%r)" % (self.asset)
    
    def __setitem__(self, key, value):
        """Create or update a property on the given asset. Overrides inherited properties.
        
        Properties set this way will not be inheritable."""
        
        self.asset._properties[key] = value
    
    def get(self, name, fallback=None, inherited=True, value=False):
        """Look up and return the given property.
        
        If inherited is False, only get the property directly from the asset.
        If value is True, don't return the Property and Asset instances, return the property's value.
        
        Returns the property and asset defining the property."""
        
        if not inherited:
            if value: return self.asset._properties[name]
            return (Property.query.filter_by(asset=self.asset).one(), self.asset)
        
        try:
            prop, asset = session.query(Property, Asset) \
                .filter(sql.or_(Property.inheritable == 1, Property.asset == self.asset)) \
                .filter(Property.name == name) \
                .filter(Property.asset_guid == Asset.guid) \
                .filter(sql.and_(Asset.l <= self.asset.l, Asset.r >= self.asset.r)) \
                .first()
            
            if prop and value: return prop.value
            return prop, asset
        
        except:
            log.exception("Error looking up property.")
            pass
        
        return fallback if value else (fallback, None)
    
    def __getitem__(self, name):
        """Lookup inherited properties using `properties['foo.bar.baz']` syntax.
        
        This can only return a single value, so we return the property value, not the property."""
        
        return self.get(name, value=True)
    
    def __delitem__(self, name):
        """Delete the given property."""
        
        prop = self.get(name, inherited=False)
        session.delete(prop)
        session.commit()


class Asset(cmf.model.Base):
    """The core of all components."""
    
    __tablename__   = "assets"
    __repr__        = lambda self: '%s %s (%s %r)' % (self.__class__.__name__, self.guid, self.name, self.title)
    __str__         = lambda self: self.name
    
    
    @property
    def Controller(self):
        from web.extras.cmf.components.asset.controller import AssetController
        return AssetController
    
    _controller     = None
    
    @property
    def controller(self):
        if not self._controller: self._controller = self.Controller(self)
        return self._controller
    
    
    @property
    def link(self):
        return "/urn:uuid:%s" % (self.guid, )
    
    @property
    def path(self):
        return "" if not self.parent else "/" + "/".join([i.name for i in self.ancestors[1:]] + [self.name])
    
'''