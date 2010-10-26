# encoding: utf-8

"""Component, theme, and extension APIs."""

from functools import wraps

from web.utils.object import CounterMeta


__all__ = ['IComponent', 'ITheme', 'IExtension', 'action', 'view']
log = __import__('logging').getLogger(__name__)



class IComponent(object):
    """Component declaration."""
    
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


class ITheme(IComponent, SingletonMixIn):
    def authorize(self, container, child):
        """Themes can not have child nodes."""
        return False


class IExtension(IComponent, SingletonMixIn):
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
    
    def __init__(self, title=None, description=None, icon=None):
        self.name = None
        
        if title: self.title = title
        if description: self.description = description
        if icon: self.icon = icon
    
    def __call__(self, f):
        from web.extras.contentment.components.asset.model import Asset
        
        kind, _, self.name = f.__name__.partition('_')
        assert kind == self.kind, "Decorator doesn't match method name.  Found %r, exepected %r." % (kind, self.kind)
        
        authorized = self.authorized
        
        @wraps(f)
        def inner(self, *args, **kw):
            if not this.authorized(self.asset, web.auth.user):
                raise web.core.http.HTTPUnauthorized
            
            template = "json:"
            data = f(*args, **kw)
            
            if isinstance(data, basestring):
                return data
            
            if isinstance(data, tuple):
                template, data = data
            
            if data is None:
                data = dict()
            
            data['root'] = Asset.objects(path='/').first()
            data['asset'] = self.asset
            
            base = '.'.join(self.__module__.split('.')[:-1]) + '.templates.'
            
            # TODO: Allow overriding of templates by the theme.
            
            return 'mako:' + base + template, data
        
        # Match wrapped function argspec.
        inner.__func_argspec__ = getattr(f, '__func_argspec__', inspect.getargspec(func))
        
        inner.authorized = self.authorized
        inner.allowed = property(self.allowed)
        
        return inner
    
    def authorized(self, entity, identity):
        """Determine if a specific entity is allowed to use this method."""
        pass


class action(Decorator):
    kind = 'action'
    pass


class view(Decorator):
    kind = 'view'
    pass


class api(Decorator):
    kind = 'api'
    pass
