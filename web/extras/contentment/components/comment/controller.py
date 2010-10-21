# encoding: utf-8

"""Basic comment controller."""

from web.extras.contentment.components.asset.controller import AssetController


log = __import__('logging').getLogger(__name__)
__all__ = ['CommentController']



class CommentController(AssetController):
    _modify_form = "web.extras.contentment.components.comment.templates.modify"
    
    def view_default(self):
        return self._template('view', base='.'.join(CommentController.__module__.split('.')[:-1]))
