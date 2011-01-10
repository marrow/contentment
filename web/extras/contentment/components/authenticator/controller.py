# encoding: utf-8

"""Basic authenticator controller.

Handle login/logout, joining, and password recovery.
"""

import web.core

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
        
        data.password = (data.password, data.yubikey)
        
        if 'redirect' not in data:
            data.redirect = '/'
        
        if not web.auth.authenticate(data.identity, data.password):
            web.core.session['flash'] = dict(cls="error", title="Authentication Failure", message="Invalid username or password.")
            return 'login', dict(redirect=data.redirect, identity=data.identity)
        
        web.core.session['flash'] = dict(cls="success", title="Success", message="Successful authentication.")
        
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
            web.core.session['flash'] = dict(cls="success", title="Success", message="Successfully signed out and cleared session.")
        
        raise web.core.http.HTTPSeeOther(
                location = web.core.request.referrer if web.core.request.referrer else '/'
            )
    
    # TODO: User management.
    # TODO: Lost password form/action.
    # TODO: Account creation form/action.
