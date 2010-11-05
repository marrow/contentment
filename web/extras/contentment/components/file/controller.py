# encoding: utf-8

"""Basic file controller."""

import web.core

from web.extras.contentment.api import action, view
from web.extras.contentment.components.asset.controller import AssetController


log = __import__('logging').getLogger(__name__)
__all__ = ['FileController']



class FileController(AssetController):
    @view('Preview', "Preview uploaded content.")
    def view_preview(self):
        return 'preview', None
    
    @view('Download', "Download this file.")
    def view_download(self):
        asset = self.asset
        response = web.core.response._current_obj()
        
        response.conditional_response = True
        response.content_type = asset.mimetype
        response.content_length = asset.size
        response.last_modified = asset.modified if asset.modified else asset.created
        response.etag = '%s-%s-%s' % (asset.modified if asset.modified else asset.created, asset.size, hash(asset.filename))
        response.app_iter = asset.content.get()
        
        return response
    
    # TODO: Raw stream.
    # TODO: Preview.  (Utilizes the embedded view.)
    # TODO: Embedded view.  (w/ handlers for application/pdf, text/*, image/*, audio/*, and video/*.)
