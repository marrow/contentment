# encoding: utf-8

"""Basic file controller."""

import webob

import web.core

from web.extras.contentment.api import action, view
from web.extras.contentment.components.asset.controller import AssetController
from web.extras.contentment.components.file.scaler import scale, get_cache, save_cache
from web.extras.contentment.components.file.reflection import add_reflection

from cStringIO import StringIO


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
        
        response.app_iter = asset.content.get()
        
        response.content_type = asset.mimetype.encode('ascii')
        response.content_length = asset.size
        response.last_modified = asset.modified if asset.modified else asset.created
        response.accept_ranges = 'bytes'
        response.etag = '%s-%s-%s' % (asset.modified if asset.modified else asset.created, asset.size, hash(filename))
        response.cache_control = 'public'
        response.content_transfer_encoding = 'binary'
        response.content_disposition = "inline" if inline else ('attachment; filename=' + filename)
        response.range = (0, asset.size)
        
        return response
    
    # TODO: Caching.
    @view('Scale', "Display a scaled version of this file.")
    def view_scale(self, filename=None, cache=True, inline=True, reflection=False, color="000000", amount=0.75, opacity=0.4, **kw):
        asset = self.asset
        
        color = '#' + color
        cache = bool(cache)
        inline = bool(inline)
        reflection = bool(reflection)
        amount = float(amount)
        opacity = float(opacity)
        
        if cache:
            id_ = str(asset.id)
            
            url = get_cache(str(asset.id), asset.modified, style="standard" if not reflection else "reflection", **kw)
            
            if url is not None:
                raise web.core.http.HTTPSeeOther(location=url)
            
            with open(save_cache(str(asset.id), asset.modified, style="standard" if not reflection else "reflection", **kw), 'wb') as fh:
                result, jquality = scale(asset.content.get(), fh, raw=reflection, **kw)
                
                if reflection:
                    result = add_reflection(result, bgcolor=color, amount=float(amount), opacity=float(opacity))
                    result.save(fh, "JPEG", optimize=True, quality=jquality)
            
            raise web.core.http.HTTPSeeOther(location=get_cache(id_, asset.modified, style="standard" if not reflection else "reflection", **kw))
        
        response = webob.Response(request=web.core.request, conditional_response=True)
        filename = asset.filename if filename is None else filename
        
        target = StringIO()
        
        result, jquality = scale(asset.content.get(), target, raw=reflection, **kw)
        
        if reflection:
            result = add_reflection(result, bgcolor=color, amount=float(amount), opacity=float(opacity))
            result.save(target, "JPEG", optimize=True, quality=jquality)
        
        response.body = target.getvalue()
        
        response.content_type = "image/jpeg"
        response.content_length = asset.size
        response.last_modified = asset.modified if asset.modified else asset.created
        response.accept_ranges = 'bytes'
        response.etag = '%s-%s-%s' % (asset.modified if asset.modified else asset.created, asset.size, hash(filename))
        response.cache_control = 'public'
        response.content_transfer_encoding = 'binary'
        response.content_disposition = "inline" if inline else ('attachment; filename=' + filename)
        
        return response
