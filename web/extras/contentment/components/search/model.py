# encoding: utf-8

import mongoengine as db
from math import log as log_

from marrow.util.convert import terms as keywords

from web.extras.contentment.components.asset.model import Asset
from web.extras.contentment.components.folder.model import Folder

from web.extras.contentment.components.asset.model.index import DocumentIndex, SearchTerm
from web.extras.contentment.components.asset.model.lexer import strip

from concurrent import futures

from widgets import fields


log = __import__('logging').getLogger(__name__)
__all__ = ['Search']



class Search(Folder):
    _widgets = fields
    
    default = db.StringField(default="view:search", max_length=128)
    
    query = db.StringField(max_length=250)
    where = db.ListField(db.StringField(max_length=250), default=lambda: ['/'])
    exclude = db.ListField(db.StringField(max_length=250), default=list)
    
    contents = property(lambda self: self.results())
    
    def results(self, query=None):
        print repr(query)
        
        if query is None: query = self.query
        if query is None: return []
        
        terms = keywords(' '.join(strip(query.lower())))
        terms = (set(terms[0] + terms[1]), set(terms[2]))
        query = dict()
        aquery = dict()
        
        print repr(terms)
        
        for term in list(terms[0]):
            if ':' in term:
                terms[0].remove(term)
                l, _, r = term.partition(':')
                
                print term, l, r
                
                if l == 'tag':
                    aquery.setdefault('tags', list()).append(r)
                
                elif l == 'kind':
                    aquery.setdefault('__raw__', dict())['_cls'] = r
        
        print aquery, terms
        
        if not terms[0] and not terms[1]:
            def gen():
                for record in Asset.objects(**aquery).only('title', 'description', 'path', 'acl').order_by('created'):
                    yield 1.0, record
            return gen()
        
        for term in terms[0]:
            query['terms__%s__exists' % (term, )] = True
        
        for term in terms[1]:
            query['terms__%s__exists' % (term, )] = False
        
        # Calculate the inverse document frequency for each term
        idfs = {}
        num_docs = DocumentIndex.objects.count()
        
        for term in terms[0]:
            term_docs = DocumentIndex.objects(terms__term=term).count()
            idfs[term] = log_((num_docs - term_docs + 0.5) / (term_docs + 0.5))
        
        # Get the average document length.
        avg_doc_length = sum([i.length for i in DocumentIndex.objects.only('length')])/float(num_docs)
        
        k = 2.0
        b = 0.75
        f = []
        results = []
        
        def compute(idfs, idx, k, b, f):
            score = 0.0
            
            for term, q in idfs.iteritems():
                dividend = idx.terms[term] * (k + 1.0)
                relDocSize = idx.length / avg_doc_length
                divisor = q + ( 1.0 - b + b * relDocSize ) * k
                termScore = (dividend / divisor) * q
                score += termScore
            
            return (score, idx.doc_id)
        
        with futures.ThreadPoolExecutor(max_workers=5) as executor:
            for idx in DocumentIndex.objects(**query):
                f.append(executor.submit(compute, idfs, idx, k, b, f))
            
            for result in futures.as_completed(f):
                score, doc_id = result.result()
                results.append((score, doc_id))
        
        def iterresults():
            for score, id_ in results:
                yield score, Asset.objects(id=id_, **aquery).only('title', 'description', 'path', 'acl').first()
        
        return sorted(iterresults(), lambda a, b: cmp(a[0], b[0]), reverse=True)
