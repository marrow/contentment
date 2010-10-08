# encoding: utf-8

"""Base asset controller.

Handles low-level navigation
"""

import re

import web

from web.core import Controller, request, session, http
from web.utils.string import normalize
from web.utils.object import yield_property

# from web.extras.contentment.core import components, action, view
# from web.extras.contentment.components.asset.core import CoreMethods


log = __import__('logging').getLogger(__name__)
__all__ = ['BaseController']



class BaseController(Controller):
    __repr__ = lambda self: '%s(%s, %s, %r)' % (self.__class__.__name__, self.asset.id, self.asset.name, self.asset.title)
    
    def __init__(self, identifier=None):
        """Initialize the controller for the given model instance."""
        
        super(BaseController, self).__init__()
        
        try:
            from web.extras.contentment.components.asset.model import Asset
            
            if isinstance(identifier, Asset): self.asset = identifier
            elif not identifier: Asset.objects(name='/', parent=None).first()
            else: self.asset = Asset.objects.with_id(identifier)
        
        except:
            log.exception("Error loading model instance for %r instance using %r.", self.__class__.__name__, identifier)
            raise http.HTTPNotFound("Unable to find resource at this location.")
        
        # TODO: Load up the actions and views for this asset.
    
    def __lookup__(self, node, *remainder, **kw):
        from web.extras.contentment.components.asset.model import Asset
        
        log.debug("Looking in %r for %r *%r...", self, node, remainder)
        
        if ":" in node:
            return self, [node.replace(":", "_")] + list(remainder)
        
        # TODO: Path-based lookup; far more efficient!
        
        if isinstance(node, basestring):
            record = Asset.objects(name=node, parent=self.asset).first()
            
            if not record:
                raise http.HTTPNotFound("Unable to find resource at this location.")
            
            return record.controller, remainder if remainder else [record.default]
        
        raise http.HTTPNotFound("Unable to find resource at this location.")


'''
    
    
    
    
    def __init__(self, guid=None):
        # Load up the actions and views for this asset.  TODO: Load them from available hooks, too, to allow extensions to extend/override base classes.
        
        def find_instances(kind):
            items = []
            
            for name in dir(self):
                value = getattr(self, name)
                #if callable(value) and name.startswith('_view_'):
                #    log.debug("Property called %r is callable: %r", name, value.__dict__)
                
                if hasattr(value, 'kind') and value.kind[0] == kind:
                    items.append((name, value))
            
            items.sort(key=lambda i: i[1]._counter, reverse=True)
            # items = [i for i in items if i[1].authorized(self.asset)]
            
            return items
        
        self.actions = find_instances('action')
        self.views = find_instances('view')
    


'''