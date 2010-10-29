# encoding: utf-8

"""Basic folder controller.

Additional views on asset contents.
"""

from web.extras.contentment.api import action, view
from web.extras.contentment.components.asset.controller import AssetController


log = __import__('logging').getLogger(__name__)
__all__ = ['SettingsController']



class SettingsController(AssetController):
    pass