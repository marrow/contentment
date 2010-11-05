# encoding: utf-8

from web.extras.contentment import release
from web.extras.contentment.api import IComponent


__all__ = ['CommentComponent', 'controller', 'model', 'templates']
log = __import__('logging').getLogger(__name__)


class CommentComponent(IComponent):
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
    def model(self):
        from web.extras.contentment.components.comment import model
        return super(CommentComponent, self).model(model)
    
    @property
    def controller(self):
        from web.extras.contentment.components.comment.controller import CommentController
        CommentController._component = self
        return CommentController
    
    def authorize(self, container, child):
        return False
    
    def authorized(self, parent):
        return False
