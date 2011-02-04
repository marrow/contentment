# encoding: utf-8

""""""

from web.extras.contentment.api import action, view
from web.extras.contentment.components.folder.controller import FolderController


log = __import__('logging').getLogger(__name__)
__all__ = ['FolderController']



class GalleryController(FolderController):
    def _scale(self, asset, scale):
        data = getattr(self.asset, scale)
        
        path = asset.path + '/view:scale/image.jpeg?'
        parts = []
        
        for i in ('xy', 'x', 'y'):
            if getattr(data, i) is not None:
                parts.append('%s=%s' % (i, getattr(data, i)))
        
        if data.square: parts.append('square=True')
        
        if data.reflect:
            parts.append('reflect=True')
            for i in ('amount', 'opacity'):
                if getattr(data, i) is not None:
                    parts.append('%s=%s' % (i, getattr(data, i)))
        
        return path + "&".join(parts)
    
    @view("Thumbnails", "An expandable thumbnail view.")
    def view_gallery(self, sort=None):
        return 'thumbnail', dict(scale=self._scale)
