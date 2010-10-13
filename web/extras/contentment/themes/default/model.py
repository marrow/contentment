# encoding: utf-8

"""Default theme model."""


import mongoengine as db

from web.extras.contentment.components.asset.model import Asset


log = __import__('logging').getLogger(__name__)
__all__ = ['DefaultTheme']
__model__ = __all__



class DefaultTheme(Asset):
    pass
