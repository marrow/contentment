# encoding: utf-8

"""Basic file controller."""

from web.extras.contentment.components.asset.controller import AssetController


log = __import__('logging').getLogger(__name__)
__all__ = ['FileController']



class FileController(AssetController):
    pass
    
    # TODO: Raw stream.
    # TODO: Rich view.  (Utilizes the embedded view.)
    # TODO: Embedded view.  (w/ handlers for application/pdf, text/*, image/*, audio/*, and video/*.)
