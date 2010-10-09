# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""


import mongoengine as db

from web.extras.contentment.components.asset.model import Asset


log = __import__('logging').getLogger(__name__)
__all__ = ['Page']
__model__ = __all__



class Page(Asset):
    content = db.StringField()
    engine = db.StringField(max_length=250, default="textile")
    template = db.StringField(max_length=250)
    
    @property
    def rendered(self):
        import web
        
        @web.core.cache.cache('page.content', expires=3600)
        def cache(name, date):
            if self.engine == 'textile':
                import textile
                return textile.textile(self.content)
            
            else:
                return self.content
        
        return cache(self.path, self.modified if self.modified else self.created)
