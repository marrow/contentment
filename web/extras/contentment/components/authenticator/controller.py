# encoding: utf-8

"""Basic authenticator controller.

Handle login/logout, joining, and password recovery.
"""

import web

from web.extras.contentment.components.asset.controller import AssetController

from marrow.util.bunch import Bunch


log = __import__('logging').getLogger(__name__)
__all__ = ['AuthenticatorController']



class LoginMethod(web.core.RESTMethod):
    def __init__(self, parent):
        super(LoginMethod, self).__init__()
        self.parent = parent
        self._template = parent._template
    
    def get(self, redirect=None):
        referrer = web.core.request.referrer
        referrer = '/' if referrer.endswith(web.core.request.script_name) else referrer
        
        if web.auth.authenticated:
            raise web.core.http.HTTPSeeOther(location=referrer)
        
        if redirect is None:
            redirect = referrer
        
        return self._template('login', dict(redirect=redirect), base='.'.join(LoginMethod.__module__.split('.')[:-1]))
    
    def post(self, ajax=False, **kw):
        data = Bunch(kw)
        
        log.info("Attempting to login as %s...", data.identity)
        
        if 'redirect' not in data:
            data.redirect = '/'
        
        if not web.auth.authenticate(data.identity, data.password):
            log.warn("Authentication failed for %s.", data.identity)
            return self._template('login', dict(redirect=redirect, identity=data.identity), base='.'.join(LoginMethod.__module__.split('.')[:-1]))
        
        raise web.core.http.HTTPFound(location=data.redirect)


class AuthenticatorController(AssetController):
    def __init__(self, *args, **kw):
        super(AuthenticatorController, self).__init__(*args, **kw)
        
        self.action_authenticate = LoginMethod(self)
    
    def action_expire(self, ajax=False):
        if web.auth.authenticated:
            web.auth.deauthenticate()
        
        raise web.core.http.HTTPSeeOther(
                location = web.core.request.referrer if web.core.request.referrer else '/'
            )
    
    # TODO: User management.
    # TODO: Lost password form/action.
    # TODO: Account creation form/action.
