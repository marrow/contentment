# encoding: utf-8

"""

Asset controller core JSON API methods.

"""

import time
from datetime import datetime

import web.core

from web.extras.contentment.components.asset.model import Asset



log = __import__('logging').getLogger(__name__)
__all__ = ['CoreMethods']



class CoreMethods(web.core.Controller):
    def __init__(self, controller):
        self.controller = controller
    
    def alterChildIndex(self, oldIndex, newIndex, **kw):
        # TODO: Security.
        
        try:
            old = int(oldIndex)
            new = int(newIndex)
            
            if old == new: return 'json:', dict(status="success", message="No change.")
            
            asset = self.controller.asset
            count = len(asset.children)
            
            if old >= count or new >= count: raise ValueError('Invalid index.')
            
            child = asset.children.pop(old)
            asset.children.insert(new, child)
            asset.save()
        
        except:
            log.exception("Error ordering child from index %s to index %s.", old, new)
            return 'json:', dict(status="error", message="Unable to re-order asset.")
        
        return 'json:', dict(status="success")
    
    def getChildren(self, kind=None, tag=None, values=None, **kw):
        request = web.core.request
        response = web.core.response
        parent = self.controller.asset
        _latest = Asset.objects(parent=parent).only('created', 'modified')
        latest = None
        
        for i in _latest:
            if latest is None or i.created > latest:
                latest = i.created
            
            if i.modified and i.modified > latest:
                latest = i.modified
        
        response.last_modified = latest
        response.cache_control = 'public'
        response.etag = "%d" % ( int(time.mktime(latest.timetuple())) if latest else 0, )
        
        if latest and request.if_modified_since and request.if_modified_since >= response.last_modified:
            raise web.core.http.HTTPNotModified()
        
        if response.etag in request.if_none_match:
            raise web.core.http.HTTPNotModified()
        
        # The scanning (esp. security) is difficult to compute.
        # So we cache the result based on the above arguments and modification times.
        # TODO: Cached for one day; this should be configurable.
        # Initial timings (with debug logging enabled!) on the following complex query:
        #   kind=gallery & values=title,path & tag=!nav:hidden
        #   W/o cache: ~50/s, w/ cache: ~72/s.
        @web.core.cache.cache('page.content', expires=86400)
        def inner(parent_id, latest, kind, tag, values, kw):
            if kind is not None:
                kind = kind.lower().split(',')
            
            if values is None: values = 'name', 'title', 'description', 'path'
            else: values = values.split(',')
            
            for i in values:
                if i not in ('name', 'title', 'description', 'path', 'kind', 'rendered', 'tags', 'children', 'descendants'):
                    return 'json:', dict(status="error", message="Forbidden.")
            
            children = []
            
            def criteria(child):
                if kind is not None and child.__class__.__name__.lower() not in kind:
                    return False
                
                if tag is not None:
                    if tag[0] != '!' and tag not in child.tags:
                        return False
                    
                    elif tag[0] == '!' and tag in child.tags:
                        return False
                
                if not child.controller.allowed:
                    return False
                
                return True
            
            try:
                for child in parent.children:
                    if not criteria(child):
                        continue
                    
                    data = dict()
                    
                    for value in values:
                        if value == 'kind':
                            data[value] = child.__class__.__name__.lower()
                            continue
                        
                        if value == 'children':
                            # We won't return the actual child objects… just if we have children or not.
                            data[value] = bool(len(Asset.objects(parent=child).only('id')))
                            continue
                        
                        if value == 'descendants':
                            # Match child objects that also meet this search criteria.
                            data[value] = bool([i for i in Asset.objects(parent=child).only('acl', 'parent', 'parents', 'tags') if criteria(i)])
                            continue
                        
                        data[value] = getattr(child, value, '')
                    
                    children.append(data)
            
            except:
                log.exception("Error iterating children.")
                return 'json:', dict(status="error", message="Error determining asset contents.")
            
            return 'json:', dict(status="success", children=children)
        
        return inner(str(parent.id), latest, kind, tag, values, kw)


"""
class CoreMethods(Controller):
    def __init__(self, controller):
        self.controller = controller
        self.tags = TagMethods(controller)
    
    def sort(self, index, **kw):
        import model
        
        index = int(index)
        
        try:
            children = self.controller.asset.parent.children.all()
            oldIndex = children.index(self.controller.asset)
            
            log.debug("Parent's children: %r", children)
            log.debug("Old index: %d  New index: %d", oldIndex, index)
            
            if index == oldIndex:
                return dict(status="warning", message="Asset should not be moved.  Did you click the handle instead of dragging it?")
            
            if index == 0:
                log.debug("Moving %r to top of child list.", self.controller.asset)
                self.controller.asset.parent.attach(self.asset, after=False, below=True)
            
            elif index == len(children) - 1:
                log.debug("Moving %r to bottom of child list.", self.controller.asset)
                self.controller.asset.parent.attach(self.asset, after=True, below=True)
            
            else:
                log.debug("Moving %r above %r.", self.controller.asset, children[index if index < oldIndex else index + 1])
                children[index if index < oldIndex else index + 1].attach(self.controller.asset, after=False, below=False)
            
        except:
            model.session.rollback()
            log.exception("Unable to move %r", self.controller.asset)
            return dict(status="error", message="Unable to move this asset.  Reload this page and try again.")
        
        model.session.commit()
        return dict(status="ok", message="Asset successfully moved.")
    
    
    def property(self, name, value=None, format='json'):
        # TODO: Security check.  Ensure the user attempting to set the property has the rights to do so.
        if format not in ['json', 'bencode']: return "Infalid format requested."
        
        try:
            if value:
                setattr(self.controller.asset, name, value)
                cmf.components.asset.model.session.commit()
                return format, dict(status="ok", message="Successfully updated property.", name=name, result=value)
            
            else:
                return format, dict(status="ok", message="Successfully retrieved property.", name=name, value=getattr(self.controller.asset, name))
        
        except:
            log.exception("Error updating property.")
            cmf.components.asset.model.session.rollback()
        
        return dict(status="error", message="Unable to update property.")


class TagMethods(Controller):
    __trailing_slash__ = False # we want .../tags to appear as a method by itself.  No trailing slash on index for us.
    
    def __init__(self, controller):
        self.controller = controller
    
    def index(self, hidden=False, format='json'):
        if format not in ['json', 'bencode']: return "Infalid format requested."
        
        return format, dict(status="ok", message="Retreived tag list.", tags=[i for i in self.controller.asset.tags if hidden or ':' not in i])

    def add(self, tag=None, format='json'):
        if tag is None: return "You must define a tag to add."
        if format not in ['json', 'bencode']: return "Infalid format requested."
        
        try:
            if tag in self.controller.asset.tags: return dict(status="warn", message="Tag already present.")
            self.controller.asset.tags.append(tag)
            cmf.components.asset.model.session.commit()
            return format, dict(status="ok", message="Added tag.", tag=tag)

        except:
            log.exception("Error adding tag.")
            cmf.components.asset.model.session.rollback()

        return format, dict(status="error", message="Unable to add tag.")

    def remove(self, tag=None, format='json'):
        if tag is None: return "You must define a tag to remove."
        if format not in ['json', 'bencode']: return "Infalid format requested."
        
        try:
            if tag not in self.controller.asset.tags: return dict(status="error", message="Tag not present.")
            self.controller.asset.tags.remove(tag)
            cmf.components.asset.model.session.commit()
            return format, dict(status="ok", message="Removed tag.", tag=tag)

        except:
            log.exception("Error adding tag.")
            cmf.components.asset.model.session.rollback()

        return format, dict(status="error", message="Unable to remove tag.")




"""