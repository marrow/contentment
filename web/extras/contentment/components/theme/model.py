# encoding: utf-8

"""Base theme model."""


import mongoengine as db

from web.extras.contentment.components.asset.model import Asset


log = __import__('logging').getLogger(__name__)
__all__ = ['Theme']
__model__ = __all__



class Theme(Asset):
    pass
