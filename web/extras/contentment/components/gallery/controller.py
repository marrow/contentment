# encoding: utf-8

""""""

from web.extras.contentment.api import action, view
from web.extras.contentment.components.folder.controller import FolderController


log = __import__('logging').getLogger(__name__)
__all__ = ['FolderController']



class GalleryController(FolderController):
    @view("Thumbnails", "An expandable thumbnail view.")
    def view_gallery(self, sort=None):
        return 'thumbnail', None
