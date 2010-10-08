from web.core                                   import session
from web.extras.cmf.api                         import IAction, IView


class Action(IAction):
    pass


class View(IView):
    pass


class AuthenticatedMixIn(object):
    def authorized(self, asset):
        # log.debug("AuthenticatedMixIn authorization: %r", session.get('cmf.authentication.account', None))
        if 'cmf.authentication.account' in session and session['cmf.authentication.account']:
            return True
        
        return False

class AuthenticatedAction(AuthenticatedMixIn, IAction):
    pass

class AuthenticatedView(AuthenticatedMixIn, IView):
    pass


class OwnerMixIn(object):
    def authorized(self, asset):
        # log.debug("OwnerMixIn authorization: %r == %r", session.get('cmf.authentication.account', None), asset.owner)
        if 'cmf.authentication.account' in session and asset.owner and asset.owner.id == session['cmf.authentication.account'].id:
            return True
        
        return False

class OwnerAction(OwnerMixIn, IAction):
    pass

class OwnerView(OwnerMixIn, IView):
    pass


class AnonymousMixIn(object):
    def authorized(self, asset):
        # log.debug("AnonymousMixIn authorization: %r", session.get('cmf.authentication.account', None))
        if 'cmf.authentication.account' not in session or not session['cmf.authentication.account']:
            return True

        return False

class AnonymousAction(AnonymousMixIn, IAction):
    pass

class AnonymousView(AnonymousMixIn, IView):
    pass
