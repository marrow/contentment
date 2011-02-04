# encoding: utf-8

"""Basic folder controller.

Additional views on asset contents.
"""

import datetime
from web.extras.contentment.api import action, view
from web.extras.contentment.components.asset.controller import AssetController


log = __import__('logging').getLogger(__name__)
__all__ = ['FolderController']



class FolderController(AssetController):
    @view("Details", "A detailed contents view.")
    def view_details(self, sort=None):
        return 'details', None
    
    @view("Gallery", "An expandable thumbnail view.")
    def view_gallery(self, sort=None):
        return 'gallery', None
    
    @view("Event Attachments", "A list of events and their attachments.")
    def view_attachments(self, year=None, sort="starts"):
        if year is None:
            year = datetime.datetime.now().year
        
        year = int(year)
        
        years = []
        
        for i in self.asset.contents:
            if not hasattr(i, 'starts'): continue
            if i.starts is None: continue
            years.append(i.starts.year)
        
        years = sorted(list(set(years)))
        
        if year > max(years):
            year = years[-1]
        
        elif year < min(years):
            yeare = years[0]
        
        filter_range = (datetime.datetime(year, 1, 1, 0, 0, 0), datetime.datetime(year+1, 1, 1, 0, 0, 0))
        
        return 'nested', dict(years=years, year=year, filter_range=filter_range, sort=sort)
