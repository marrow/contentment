# encoding: utf-8

import mongoengine as db

from marrow.util.convert import terms as keywords

from web.extras.contentment.components.asset.model import Asset
from web.extras.contentment.components.folder.model import Folder


log = __import__('logging').getLogger(__name__)
__all__ = ['Search']



class Search(Folder):
    default = db.StringField(default="view:search", max_length=128)
    
    query = db.StringField(max_length=250)
    where = db.ListField(db.StringField(max_length=250), default=lambda: ['/'])
    exclude = db.ListField(db.StringField(max_length=250), default=list)
    
    contents = property(lambda self: self.results())
    
    def results(self, query=None):
        if query is None: query = self.query
        if query is None: return []
        
        terms = keywords(query.lower())
        terms = (set(terms[0] + terms[1]), set(terms[2]))
        query = {}
        
        for term in list(terms[0]):
            # if ':' in term:
            #     terms[0].remove(term)
            
            if term.startswith('tag:'):
                if 'tags__all' not in query: query['tags__all'] = []
                query['tags__all'].append(term[4:])
        
        if terms[0]: query['index__in'] = terms[0]
        if terms[1]: query['index__nin'] = terms[1]
        
        return Asset.objects(**query)
