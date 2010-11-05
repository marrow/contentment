# encoding: utf-8

"""Basic comment controller."""

from web.extras.contentment.api import action, view
from web.extras.contentment.components.asset.controller import AssetController


log = __import__('logging').getLogger(__name__)
__all__ = ['CommentController']



class CommentController(AssetController):
    @view("Comment", "Display comment with replies.")
    def view_comment(self):
        return 'view', None
