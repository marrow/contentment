# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""

import re
import web
import pytz

from datetime import datetime
from copy import copy, deepcopy
from collections import defaultdict

import mongoengine as db

from web.extras.contentment.components.asset.widgets import fields
from web.extras.contentment.components.asset.model.index import SearchTerm, DocumentIndex
from marrow.util.bunch import Bunch
from acl import *
import lexer


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



class Asset(db.Document):
    def __repr__(self):
        return '%s(%s, "%s")' % (self.__class__.__name__, self.path, self.title)
    
    meta = dict(
            collection="assets",
            ordering=['parents', 'name'],
            indexes=[('parents', 'name'), 'parent', 'name', 'path', 'owner', 'created', 'modified']
        )
    
    _indexable = dict(title=10.0, description=5.0, tags=8.5)
    _widgets = fields
    
    _component = None
    controller = None
    
    id = db.ObjectIdField('_id')
    
    # Relationship information.
    parent = db.GenericReferenceField(default=None)
    parents = db.ListField(db.GenericReferenceField(), default=list)
    children = db.ListField(db.GenericReferenceField(), default=list)
    contents = property(lambda self: Asset.objects(parent=self))
    path = db.StringField(default='')
    
    # Basic properties.
    name = db.StringField(max_length=250, required=True) # unique_with="parent"
    title = db.StringField(max_length=250, required=True)
    description = db.StringField()
    
    # Magic properties.
    immutable = db.BooleanField(default=False)
    default = db.StringField(default="view:contents", max_length=128)
    tags = db.ListField(db.StringField(max_length=32), default=list)
    properties = db.DictField(default=dict)
    acl = db.ListField(db.EmbeddedDocumentField(ACLRule), default=list)
    template = db.StringField(max_length=250, default='')
    
    # Ownership and dates.
    owner = db.GenericReferenceField()
    created = db.DateTimeField(default=lambda: datetime.utcnow().replace(microsecond=0, tzinfo=pytz.utc))
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
        
        for rule in root.acl:
            if not isinstance(rule, InheritACLRules):
                yield root, rule
                continue
            
            for node in reversed(nodes):
                for rule in node.acl:
                    yield node, rule
    
    def _form(self, action, submit="Save", referrer=None):
        from alacarte.template.simplithe.widgets import Form, FieldSet, DefinitionListLayout, FileField
        from web.extras.contentment.widgets import ContentmentFooter
        
        order = []
        groups = {}
        seen = []
        enctype = None
        
        for base in reversed(type.mro(type(self))):
            try:
                widgets = getattr(base, '_widgets', None)
                if not widgets or widgets in seen or not hasattr(widgets, '__call__'): continue
                seen.append(widgets)
                
                for name, title, fields in widgets(self):
                    if name not in groups:
                        order.append(name)
                        groups[name] = FieldSet(name, title, DefinitionListLayout, children=copy(fields))
                        continue
                    
                    groups[name].children.extend(copy(fields))
                    
                    for field in fields:
                        if isinstance(field, FileField):
                            enctype = "multipart/form-data"
            
            except AttributeError:
                pass
        
        if 'properties' in order:
            order.remove('properties')
            order.append('properties')
        
        if 'security' in order:
            order.remove('security')
            order.append('security')
        
        return Form('asset', action=action, enctype=enctype, footer=ContentmentFooter('asset', submit, referrer=referrer), children=[groups[i] for i in order])
    
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
            node.path = '/' + '/'.join([i.name for i in node.parents][1:] + [node.name])
            
            if node.children:
                nodes.extend(node.children)
            
            node.save()
    
    def reindex(self, dirty=None):
        # Determine indexable attributes and their weights.
        indexable = {}
        
        for base in reversed(type.mro(type(self))):
            _ = getattr(base, '_indexable', {})
            
            if isinstance(_, dict):
                indexable.update(_)
            
            elif isinstance(_, list):
                indexable.update(dict.fromkeys(_, 1.0))
        
        # Determine if we actually need to re-index or not.
        if dirty is not None and not set(indexable.keys()).intersection(set(dirty)):
            return
        
        index = DocumentIndex.objects(doc_id=self.id).first()
        if index: index.delete()
        
        # Determine the number of occurrences of each term with a per-attribute weight.
        occurrences = defaultdict(float)
        
        for attr, weight in indexable.iteritems():
            value = getattr(self, attr)
            
            if isinstance(value, basestring):
                for word in lexer.strip(value):
                    occurrences[word] += weight
            
            elif isinstance(value, (tuple, list, set)):
                for word in lexer.strip(u' '.join(value).encode('utf8')):
                    occurrences[word] += weight
        
        # Save the index and terms.
        index = DocumentIndex(doc_id=str(self.id), length=len(occurrences), terms=occurrences)
        index.save(safe=False)
    
    def save(self, safe=True, force_insert=False, validate=True, dirty=None):
        if not dirty:
            return super(Asset, self).save(safe=safe, force_insert=force_insert, validate=validate)
        
        result = super(Asset, self).save(safe=safe, force_insert=force_insert, validate=validate)
        
        self.reindex(dirty)
        
        result = super(Asset, self).save(safe=safe, force_insert=force_insert, validate=validate)
        
        if dirty and 'name' in dirty:
            log.debug("Re-naming asset %r...", self)
            self.path = '/' + '/'.join([i.name for i in self.parents][1:] + [self.name])
            
            super(Asset, self).save(safe=safe, force_insert=force_insert, validate=validate)
            
            nodes = list(self.children)
            
            while nodes:
                node = nodes.pop()
                node.path = '/' + '/'.join([i.name for i in node.parents][1:] + [node.name])
                
                if node.children:
                    nodes.extend(node.children)
                
                node.save()
    
    def delete(self, safe=False):
        # Delete index data, if any.
        index = DocumentIndex.objects(id=self.id).first()
        if index: index.delete()
        
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
    
    def prepare(self):
        data = self._data
        
        for n, i in enumerate(self.acl):
            if isinstance(i, PublicationACLRule):
                data['acl.publish'] = i.publish
                data['acl.retract'] = i.retract
                continue
            
            if isinstance(i, AllUsersACLRule) and not i.allow and n != len(self.acl):
                data['acl.private'] = True
                continue
            
            if isinstance(i, AuthenticatedUsersACLRule) and i.permission == "view:*" and i.allow == True:
                data['acl.member'] = True
                continue
        
        return data
    
    def process(self, formdata):
        result = []
        acl = Bunch()
        
        for name in list(formdata):
            if name.startswith('acl.'):
                acl[name.partition('.')[2]] = formdata.pop(name)
        
        if self.path in ['/', '/settings']:
            return formdata
        
        if acl.private:
            result.append(AllUsersACLRule(permission="*", allow=False))
        
        if acl.member:
            result.append(AuthenticatedUsersACLRule(permission="view:*", allow=True))
        
        if acl.publish or acl.retract:
            log.info("%r", acl)
            result.append(PublicationACLRule(permission="view:*", allow=True, publish=acl.publish, retract=acl.retract))
        
        if result:
            result.append(AllUsersACLRule(permission="*", allow=False))
        
        self.acl = result
        
        # if acl.member:
        #     pass
        # 
        # else:
        #     pass
        # 
        return formdata


class ChangeSet(db.Document):
    meta = dict(
            collection="changesets",
            ordering=['asset', 'date'],
            indexes=[('asset', 'date')]
        )
    
    id = db.ObjectIdField('_id')
    
    asset = db.ReferenceField(Asset)
    date = db.DateTimeField(default=lambda: datetime.utcnow().replace(microsecond=0))
    changes = db.DictField(default=dict)
