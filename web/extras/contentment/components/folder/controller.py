# encoding: utf-8

"""Basic folder controller.

Additional views on asset contents.
"""

from web.extras.contentment.components.asset.controller import AssetController


log = __import__('logging').getLogger(__name__)
__all__ = ['FolderController']



class FolderController(AssetController):
    # @view("Contents") # TODO: Roll above code into @view/action decorator.
    def view_details(self, sort=None):
        return self._template('details', base='.'.join(FolderController.__module__.split('.')[:-1]))
    
