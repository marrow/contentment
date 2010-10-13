# encoding: utf-8

"""Component, theme, and extension APIs."""


__all__ = ['IComponent', 'ITheme', 'IExtension']
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
        
        for name in dir(module):
            attr = getattr(module, name)
            
            if not issubclass(attr, Asset):
                continue
            
            attr._component = self
            
            # Allow overriding of the assigned controller class.
            # NOTE: This prohibits the use of an attribute called 'controller' in the schema!
            if not getattr(j, 'controller', None):
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
        
        return not model.objects


class ITheme(IComponent, SingletonMixIn):
    def authorize(self, container, child):
        """Themes can not have child nodes."""
        return False


class IExtension(IComponent, SingletonMixIn):
    def authorize(self, container, child):
        """Extensions can not have child nodes."""
        return False
