# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""

import re

import web

from datetime import datetime

import mongoengine as db

from widgets import fields

from copy import copy, deepcopy


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



particles = u"""able abst added almost alone along already also although always among amongst and announce another any anybody anyhow anymore anyone anything anyway anyways anywhere apparently approximately are aren arent aren't arise around aside ask asking auth available away awfully back became because become becomes becoming been before beforehand begin beginning beginnings begins behind being believe below beside besides between beyond biol both brief briefly but came can cannot can't cause causes certain certainly come comes contain containing contains could couldnt date did didn't different does doesn't doing done don't down downwards due during each edu effect eight eighty either else elsewhere end ending enough especially et-al etc even ever every everybody everyone everything everywhere except far few fifth first five fix followed following follows for former formerly forth found four from further furthermore gave get gets getting give given gives giving goes gone got gotten had happens hardly has hasn't have haven't having hed hence her here hereafter hereby herein heres hereupon hers herself hes hid him himself his hither home how howbeit however hundred i'll i'm immediate immediately importance important indeed index information instead into invention inward isn't itd it'd it'll its itself i've just jk keep keeps kept keys know known knows largely last lately later latter latterly least less lest let lets like liked likely line little 'll look looking looks ltd made mainly make makes many may maybe mean means meantime meanwhile merely might million miss more moreover most mostly mrs much mug must myself name namely nay near nearly necessarily necessary need needs neither never nevertheless new next nine ninety nobody non none nonetheless noone nor normally nos not noted nothing now nowhere obtain obtained obviously off often okay old omitted once one ones only onto ord other others otherwise ought our ours ourselves out outside over overall owing own page pages part particular particularly past per perhaps placed please plus poorly possible possibly potentially predominantly present previously primarily probably promptly proud provides put que quickly quite ran rather readily really recent recently ref refs regarding regardless regards related relatively research respectively resulted resulting results right run said same saw say saying says sec section see seeing seem seemed seeming seems seen self selves sent seven several shall she shed she'll shes should shouldn't show showed shown showns shows significant significantly similar similarly since six slightly some somebody somehow someone somethan something sometime sometimes somewhat somewhere soon sorry specifically specified specify specifying still stop strongly sub substantially successfully such sufficiently suggest sup sure take taken taking tell tends than thank thanks thanx that that'll thats that've the their theirs them themselves then thence there thereafter thereby thered therefore therein there'll thereof therere theres thereto thereupon there've these they theyd they'll theyre they've think this those thou though thoughh thousand throug through throughout thru thus til tip to together too took toward towards tried tries truly try trying twice two under unfortunately unless unlike unlikely until unto up upon ups us use used useful usefully usefulness uses using usually value various 've very via viz vol vols want wants was wasn't way wed welcome we'll went were weren't we've what whatever what'll whats when whence whenever where whereafter whereas whereby wherein wheres whereupon wherever whether which while whim whither who whod whoever whole who'll whom whomever whos whose why widely willing wish with within without won't words world would wouldn't www yes yet you youd you'll your youre yours yourself yourselves you've zero what're""".split()
particles = []


class ACLRule(db.EmbeddedDocument):
    def __str__(self):
        return self.__class__.__name__

class InheritACLRules(ACLRule):
    pass

class BaseACLRule(ACLRule):
    def __str__(self):
        return self.__class__.__name__ + "(" + ("allow" if self.allow else "deny") + ", " + self.permission + ")"
    
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

class AdvancedACLRule(BaseACLRule):
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
    
    attributes = db.DictField(default=dict)



class Asset(db.Document):
    def __repr__(self):
        return '%s(%s, "%s")' % (self.__class__.__name__, self.path, self.title)
    
    meta = dict(
            collection="assets",
            ordering=['parents', 'name'],
            indexes=[('parents', 'name'), 'parent', 'name', 'path', 'index', 'owner', 'created', 'modified']
        )
    
    _indexable = ['title', 'description', 'tags']
    _widgets = fields
    
    _component = None
    controller = None
    
    id = db.ObjectIdField('_id')
    
    # Relationship information.
    parent = db.GenericReferenceField(default=None)
    parents = db.ListField(db.GenericReferenceField(), default=list)
    children = db.ListField(db.GenericReferenceField(), default=list)
    contents = property(lambda self: Asset.objects(parent=self))
    path = db.StringField(default="/")
    
    # Basic properties.
    name = db.StringField(max_length=250, required=True) # unique_with="parent"
    title = db.StringField(max_length=250, required=True)
    description = db.StringField()
    
    # Search
    index = db.ListField(db.StringField(), default=[])
    
    # Magic properties.
    immutable = db.BooleanField(default=False)
    default = db.StringField(default="view:contents", max_length=128)
    tags = db.ListField(db.StringField(max_length=32), default=list)
    properties = db.DictField(default=dict)
    acl = db.ListField(db.EmbeddedDocumentField(ACLRule), default=list)
    
    # Ownership and dates.
    owner = db.GenericReferenceField()
    created = db.DateTimeField(default=lambda: datetime.utcnow().replace(microsecond=0))
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
        from alacarte.template.simplithe.widgets import Form, FieldSet, DefinitionListLayout
        from web.extras.contentment.widgets import ContentmentFooter
        
        order = []
        groups = {}
        seen = []
        
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
            
            except AttributeError:
                pass
        
        return Form('asset', action=action, footer=ContentmentFooter('asset', submit, referrer=referrer), children=[groups[i] for i in order])
    
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
    
    def save(self, safe=True, force_insert=False, validate=True, dirty=None):
        if not dirty:
            return super(Asset, self).save(safe=safe, force_insert=force_insert, validate=validate)
        
        # Re-index indexable columns.
        # TODO: Store as dict of {name: occurances} for search result weighting.
        index = []
        
        indexable = []
        for base in reversed(type.mro(type(self))):
            indexable.extend(getattr(base, '_indexable', []))
        
        indexable = set(indexable)
        
        if not indexable.union(set(dirty)):
            return super(Asset, self).save(safe=safe, force_insert=force_insert, validate=validate)
        
        for i in indexable:
            value = getattr(self, i)
            
            if isinstance(value, basestring):
                for i in value.split():
                    stripped = i.lower().strip(' \t.,\'"()[]{}<>-?!:;*/\\^').replace("'s", "")
                    if len(stripped) < 3 or stripped in particles: continue
                    index.append(stripped)
            
            elif isinstance(value, (tuple, list, set)):
                index.extend(value)
        
        self.index = list(set(index))
        
        return super(Asset, self).save(safe=safe, force_insert=force_insert, validate=validate)
    
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
    date = db.DateTimeField(default=lambda: datetime.utcnow().replace(microsecond=0))
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