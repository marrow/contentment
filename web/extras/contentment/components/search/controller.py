# encoding: utf-8

"""Basic search controller.

Site-wide search and saved searches.
"""

import web

from web.extras.contentment.api import action, view
from web.extras.contentment.components.folder.controller import FolderController


log = __import__('logging').getLogger(__name__)
__all__ = ['SearchController']



class SearchController(FolderController):
    @view("Search", "Display a search form and search results.")
    def view_default(self, q=None):
        asset = self.asset
        
        if q is None: q = asset.query
        results = asset.results(q)
        
        return 'search', dict(q=q if q else "", results=results, count=len(results))
