# encoding: utf-8

"""Basic alias controller.

Referral tracking and link aggregation.
"""

import web

from web.extras.contentment.api import action, view
from web.extras.contentment.components.asset.controller import AssetController


log = __import__('logging').getLogger(__name__)
__all__ = ['AliasController']



class AliasController(AssetController):
    @view("Redirect", "Redirect automatically to a new location.")
    def view_default(self, sort=None):
        # TODO: Track link usage.
        # TODO: Optionally track via session.
        raise web.core.http.HTTPSeeOther(location=self.asset.target)
