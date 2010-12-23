# encoding: utf-8

"""Component, theme, and extension APIs."""

import inspect
import tempfile

from functools import wraps

import web

from web.utils.object import CounterMeta


__all__ = ['IComponent', 'ITheme', 'IExtension', 'action', 'view']
log = __import__('logging').getLogger(__name__)



class IComponent(object):
    """A high-level component comprised of a controller and at least one descendant of the Asset model.
    
    A component ties these two primary elements together; when an instance of the Asset descendant is loaded, the controller identified here is used to process front-end requests.
    """
    
    title = None
    summary = None
    description = None
    icon = None
    group = None
    
    version = None
    author = None
    email = None
    url = None
    copyright = None
    license = None
    
    enabled = True
    
    def model(self, module=None):
        """Return the prepared model for this component.
        
        Override this in a subclass, make it a @property, and call thus:
        
            from ...mycomponent import model as module
            return super(MyComponent, self).model(module)
        """
        
        from web.extras.contentment.components.asset.model import Asset
        
        models = dict()
        
        for name in module.__all__:
            attr = getattr(module, name)
            
            try:
                if not issubclass(attr, Asset):
                    continue
            
            except:
                continue
            
            attr._component = self
            
            # Allow overriding of the assigned controller class.
            # NOTE: This prohibits the use of an attribute called 'controller' in the schema!
            if not getattr(attr, 'controller', None):
                attr.controller = property(lambda self: self._component.controller(self))
            
            models[name] = attr
        
        return models
    
    @property
    def controller(self):
        """Return the primary controller for this component.
        
        Do not call super for this method.
        """
        
        raise NotImplementedError
    
    def authorize(self, container, child):
        """Called once per component type.
        
        This method allows you to programatically determine which component types are allowed as children of this component.
        
        Passed an instance of this component's model and the IComponent subclass to validate.
        """
        
        return True
    
    def authorized(self, parent):
        """Called to determine if an instance of this component can be placed within a specific parent.
        
        Allows potential child nodes to exclude themselves.
        """
        
        return True


class SingletonMixIn(object):
    def authorized(self, parent):
        models = self.model
        
        assert len(models) == 1, "Singletons must only have one primary model."
        
        model = list(models.itervalues())[0]
        
        return not len(model.objects)


class ITheme(SingletonMixIn, IComponent):
    def authorized(self, parent):
        """Only one theme may be active at a time."""
        from web.extras.contentment.components.theme.model import Theme
        return not len(Theme.objects)
    
    def authorize(self, container, child):
        """Themes can not have child nodes."""
        return False


class IExtension(SingletonMixIn, IComponent):
    def authorize(self, container, child):
        """Extensions can not have child nodes."""
        return False





class Decorator(object):
    """Implements method security, convienent template lookup, and theme-override of templates."""
    
    __metaclass__ = CounterMeta
    
    kind = None
    
    title = None
    description = None
    icon = None
    
    def __init__(self, title=None, description=None, icon=None, name=None):
        self.name = name
        
        if title: self.title = title
        if description: self.description = description
        if icon: self.icon = icon
    
    def __call__(self, f):
        from web.extras.contentment.components.asset.model import Asset
        
        if not self.name:
            kind, _, self.name = f.__name__.partition('_')
            assert kind == self.kind, "Decorator doesn't match method name.  Found %r, exepected %r." % (kind, self.kind)
        
        name = self.name
        authorized = self.authorized
        
        @wraps(f)
        def inner(self, *args, **kw):
            if not authorized(self.asset):
                raise web.core.http.HTTPUnauthorized
            
            template = "json:"
            data = f(self, *args, **kw)
            
            if not isinstance(data, tuple):
                return data
            
            template, data = data
            
            if data is None:
                data = dict()
            
            root = data['root'] = Asset.objects(path='/').first()
            asset = data['asset'] = self.asset
            
            if not asset.template:
                data['template'] = root.properties.get('org-contentment-default-template', root.properties['org-contentment-theme'] + '.templates.master')
            
            elif asset.template == ':none':
                data['template'] = root.properties['org-contentment-theme'] + '.templates.master'
            
            if data.get('template', asset.template)[0] == '/':
                template_ = Asset.objects(path=data.get('template', asset.template)).first()
                
                if template_:
                    fh = tempfile.NamedTemporaryFile(mode='wb', prefix='contentment-template-', suffix='.html', delete=False)
                    fh.write('<%inherit file="' + root.properties['org-contentment-theme'] + '.templates.master"/>\n' + template_.content)
                    fh.close()
                    
                    data['template'] = fh.name
                
                else:
                    data['template'] = root.properties['org-contentment-theme'] + '.templates.master'
            
            base = '.'.join(f.__module__.split('.')[:-1]) + '.templates.'
            
            # TODO: Allow overriding of templates by the theme.
            
            return 'mako:' + base + template, data
        
        # Match wrapped function argspec.
        inner.__func_argspec__ = getattr(f, '__func_argspec__', inspect.getargspec(f))
        
        inner._counter = self._counter
        inner.kind = kind
        inner.name = name
        inner.name_ = kind + ":" + name
        inner.title = self.title
        inner.description = self.description
        inner.icon = self.icon
        inner.authorized = self.authorized
        
        return inner
    
    def authorized(self, entity, identity=None):
        """Determine if a specific entity is allowed to use this method."""
        
        if identity is None:
            identity = web.auth.user.identity if web.auth.user else None
        
        for owner, rule in entity.acl_:
            result = rule(entity, identity, self.kind, self.name)
            
            if result is True:
                return True
            
            if result is False:
                return False
        
        # Just to be safe.
        return False


class action(Decorator):
    kind = 'action'


class view(Decorator):
    kind = 'view'


class api(Decorator):
    kind = 'api'
