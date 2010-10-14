# encoding: utf-8

from web.extras.contentment import release


__all__ = ['CommentComponent', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class CommentComponent(object):
    """"""
    
    title = "Comment"
    summary = None
    description = None
    icon = 'base-comment'
    group = "Basic Types"
    
    version = release.version
    author = release.author
    email = release.email
    url = release.url
    copyright = release.copyright
    license = release.license
    
    @property
    def enabled(self):
        return True
    
    @property
    def model(self):
        from web.extras.contentment.components.asset.model import Asset
        from web.extras.contentment.components.comment import model
        
        models = dict([(i, getattr(model, i)) for i in model.__model__])
        
        for i, j in models.iteritems():
            if issubclass(j, Asset):
                j._component = self
                
                if not getattr(j, 'controller', None):
                    # We allow overriding of this.
                    j.controller = property(lambda self: self._component.controller(self))
        
        return models
    
    @property
    def controller(self):
        from web.extras.contentment.components.comment.controller import CommentController
        CommentController._component = self
        return CommentController
    
    def constructor(self, **kw):
        """A factory method to create new instances of this component."""
        from web.extras.contentment.components.comment.model import Comment
        return Comment(**kw)
    
    def authorize(self, child):
        return False # TODO: Check for File instance and allow.

