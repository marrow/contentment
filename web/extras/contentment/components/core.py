# encoding: utf-8

"""Base asset controller.

Handles low-level navigation
"""

import re

import web
import web.auth

from web.core import Controller, request, session, http
from web.utils.string import normalize
from web.utils.object import yield_property

from web.extras.contentment.core import components, models

# from web.extras.contentment.core import components, action, view
# from web.extras.contentment.components.asset.core import CoreMethods


log = __import__('logging').getLogger(__name__)
__all__ = ['BaseController']



class BaseController(Controller):
    __repr__ = lambda self: '%s(%s, "%s")' % (self.__class__.__name__, self.asset.path, self.asset.title)
    
    @property
    def _create_types(self):
        asset = self.asset
        allowed = []
        
        for name, component in components.iteritems():
            if not component.authorized(asset):
                continue
            
            if not asset._component.authorize(asset, component):
                continue
            
            yield name, component
    
    @property
    def asset(self):
        from web.extras.contentment.components.asset.model import Asset
        
        identifier = self._identifier
        
        try:
            if isinstance(identifier, Asset): return identifier
            elif identifier is not None: return Asset.objects.with_id(identifier)
            
            return Asset.objects(path='/').first()
        
        except:
            log.exception("Error loading model instance for %r instance using %r.", self.__class__.__name__, identifier)
            raise http.HTTPNotFound("Unable to find resource at this location.")
    
    def __init__(self, identifier=None):
        """Initialize the controller for the given model instance."""
        
        self._identifier = identifier
        
        super(BaseController, self).__init__()
        
        def find_instances(kind):
            items = []
            
            for name in dir(self):
                if not name.startswith('action_') and not name.startswith('view_') and not name.startswith('api_'):
                    continue
                
                try:
                    value = getattr(self, name)
                
                except:
                    continue
                
                if hasattr(value, 'kind') and value.kind == kind:
                    items.append(value)
            
            items.sort(key=lambda i: i._counter)
            
            return items
        
        self.actions = find_instances('action')
        self.views = find_instances('view')
    
    def __lookup__(self, *remainder, **kw):
        from web.extras.contentment.components.asset.model import Asset
        
        asset = self.asset
        
        if not remainder:
            return self, [asset.default]
        
        remainder = list(remainder)
        
        if asset.path == '/' and remainder == ['sitemap.xml']:
            return self, ['sitemap_xml']
        
        if web.core.request.script_name == '':
            # Path-based lookup, used only when starting from the site root.
            
            paths = []
            
            for i in xrange(1, len(remainder) + (0 if ':' in remainder[-1] else 1)):
                paths.append('/' + '/'.join(remainder[:i]))
            
            nearest = Asset.objects(path__in=paths).order_by('-path').first()
            
            if nearest:
                consumed = paths.index(nearest.path) + 1
                
                remainder = remainder[consumed:]
                for i in range(consumed):
                    web.core.request.path_info_pop()
                
                return nearest.controller, remainder if remainder else [nearest.default]
        
        # Attribute-based lookup.
        
        node = remainder.pop(0).replace('%3A', ':')
        
        log.debug("Looking in %r for %r *%r...", self, node, remainder)
        
        if ":" in node:
            return self, [node.replace(":", "_")] + list(remainder)
        
        if isinstance(node, basestring):
            record = Asset.objects(name=node, parent=asset).first()
            
            if not record:
                raise http.HTTPNotFound("Unable to find resource at this location.")
            
            web.core.request.path_info_pop()
            
            return record.controller, remainder if remainder else [record.default]
        
        raise http.HTTPNotFound("Unable to find resource at this location.")
