# encoding: utf-8

"""Basic authenticator controller.

Handle login/logout, joining, and password recovery.
"""

import web

from web.extras.contentment.api import action, view
from web.extras.contentment.components.asset.controller import AssetController

from marrow.util.bunch import Bunch


log = __import__('logging').getLogger(__name__)
__all__ = ['AuthenticatorController']



class LoginMethod(web.core.RESTMethod):
    def get(self, redirect=None):
        referrer = web.core.request.referrer or '/'
        referrer = '/' if referrer.endswith(web.core.request.script_name) else referrer
        
        if web.auth.authenticated:
            raise web.core.http.HTTPSeeOther(location=referrer)
        
        if redirect is None:
            redirect = referrer
        
        return 'login', dict(redirect=redirect)
    
    def post(self, ajax=False, **kw):
        data = Bunch(kw)
        
        log.info("Attempting to login as %s...", data.identity)
        
        if 'redirect' not in data:
            data.redirect = '/'
        
        if not web.auth.authenticate(data.identity, data.password):
            log.warn("Authentication failed for %s.", data.identity)
            return 'login', dict(redirect=data.redirect, identity=data.identity)
        
        raise web.core.http.HTTPFound(location=data.redirect)


class AuthenticatorController(AssetController):
    _action = LoginMethod()
    
    @action("Sign In", "Sign into an account on this site.")
    def action_authenticate(self, *args, **kw):
        return self._action(*args, **kw)
    
    @action("Sign Out", "Expire your session, signing you out.")
    def action_expire(self, ajax=False):
        if web.auth.authenticated:
            web.auth.deauthenticate()
        
        raise web.core.http.HTTPSeeOther(
                location = web.core.request.referrer if web.core.request.referrer else '/'
            )
    
    # TODO: User management.
    # TODO: Lost password form/action.
    # TODO: Account creation form/action.
