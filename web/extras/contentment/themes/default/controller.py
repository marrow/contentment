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
__all__ = ['DefaultThemeController']



class DefaultThemeController(AssetController):
    """"""
    
    def static(self, *parts, **kw):
        # Return static content!  Or, at least, try to.
        # Our static file path is present in self._component.path + 'public'.
        
        base = os.path.join(self._component.path, 'public')
        path = os.path.normpath(os.path.join(base, *parts))
        
        log.debug(path)
        
        if not path.startswith(base):
            raise web.core.http.HTTPForbidden()
        
        elif not os.path.isfile(path):
            raise web.core.http.HTTPNotFound()
        
        request = web.core.request._current_obj()
        response = web.core.response._current_obj()
        
        # Convert to UTC.
        modified = time.mktime(time.gmtime(os.path.getmtime(path)))
        
        response.content_type, response.content_encoding = mimetypes.guess_type(path)
        response.content_length = os.path.getsize(path)
        response.etag = "%d" % ( modified, )
        
        if web.core.request.method == 'HEAD':
            return ''
        
        if response.etag in request.if_none_match:
            log.debug("Raising not modified.")
            raise web.core.http.HTTPNotModified()
        
        def iterable():
            with open(path, 'rb', 0) as f:
                while True:
                    data = f.read(4096)
                    yield data
                
                    if len(data) < 4096:
                        break
        
        return iterable()
