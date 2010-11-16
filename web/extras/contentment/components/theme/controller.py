# encoding: utf-8

"""Default theme controller."""

from __future__ import with_statement

import os
import sys
import time
import datetime
import mimetypes

import web

from web.extras.contentment.components.asset.controller import AssetController


log = __import__('logging').getLogger(__name__)
__all__ = ['ThemeController']



class ThemeController(AssetController):
    def static(self, *parts, **kw):
        # Return static content!  Or, at least, try to.
        # Our static file path is present in self._component.path + 'public'.
        
        base = os.path.join(self._component.path, 'public')
        path = os.path.normpath(os.path.join(base, *parts))
        
        if not path.startswith(base):
            raise web.core.http.HTTPForbidden("Cowardly refusing to violate base path policy.")
        
        if not os.path.exists(path):
            raise web.core.http.HTTPNotFound()
        
        if not os.path.isfile(path):
            raise web.core.http.HTTPForbidden("Cowardly refusing to open a non-file.")
        
        request = web.core.request._current_obj()
        response = web.core.response._current_obj()
        
        modified = time.mktime(time.gmtime(os.path.getmtime(path)))
        
        response.last_modified = datetime.datetime.fromtimestamp(modified)
        response.cache_control = 'public'
        
        response.content_type, response.content_encoding = mimetypes.guess_type(path)
        response.content_length = os.path.getsize(path)
        response.etag = "%d" % ( modified, )
        
        if request.if_modified_since and request.if_modified_since >= response.last_modified:
            raise web.core.http.HTTPNotModified()
        
        if web.core.request.method == 'HEAD':
            return ''
        
        if response.etag in request.if_none_match:
            raise web.core.http.HTTPNotModified()
        
        def iterable():
            with open(path, 'rb', 0) as f:
                while True:
                    data = f.read(4096)
                    yield data
                
                    if len(data) < 4096:
                        break
        
        return iterable()
