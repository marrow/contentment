# encoding: utf-8

"""Basic file controller."""

import webob

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
    def view_download(self, filename=None, inline=False):
        asset = self.asset
        response = webob.Response(request=web.core.request, conditional_response=True)
        filename = asset.filename if filename is None else filename
        
        response.content_type = asset.mimetype
        response.content_length = asset.size
        response.last_modified = asset.modified if asset.modified else asset.created
        response.accept_ranges = 'bytes'
        response.etag = '%s-%s-%s' % (asset.modified if asset.modified else asset.created, asset.size, hash(filename))
        response.cache_control = 'public'
        response.content_transfer_encoding = 'binary'
        response.content_disposition = "inline" if inline else ('attachment; filename=' + filename)
        response.range = (0, asset.size)
        
        response.app_iter = asset.content.get()
        
        return response
    
    # TODO: Raw stream.
    # TODO: Preview.  (Utilizes the embedded view.)
    # TODO: Embedded view.  (w/ handlers for application/pdf, text/*, image/*, audio/*, and video/*.)
