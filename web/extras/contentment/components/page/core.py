# encoding: utf-8

"""

Page controller JSON API methods.

"""

import web.core



log = __import__('logging').getLogger(__name__)
__all__ = ['PageMethods']



class PageMethods(web.core.Controller):
    def __init__(self, controller):
        self.controller = controller
    
    def getRendered(self, filename=None, mime="text/plain"):
        if mime not in ('text/plain', 'text/html', 'text/css', 'application/x-javascript'):
            raise web.core.exc.HTTPNotAuthorized()
        
        web.core.response.content_type = mime
        return self.controller.asset.rendered