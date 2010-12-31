# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""

import re
import web
import textile

import mongoengine as db

from web.extras.contentment.components.asset.model import Asset

from widgets import fields


log = __import__('logging').getLogger(__name__)
__all__ = ['Page']



class Page(Asset):
    _indexable = ['_content']
    _widgets = fields
    
    default = db.StringField(default="view:page", max_length=128)
    
    content = db.StringField()
    engine = db.StringField(max_length=250, default="textile")
    related = db.ListField(db.ReferenceField(Asset), default=list)
    
    attachments = db.BooleanField(default=True)
    
    @property
    def rendered(self):
        content = self.content
        
        # Determine substitutions and associated asset dates.
        replacements = []
        
        if self.engine not in ['raw', 'mako']:
            find = self.content.find
            index = find('${')
            while index != -1:
                newline = find('\n', index)
                close = find('}', index)
            
                if close == -1 or (newline != -1 and newline < close):
                    return """<div class="error">Error parsing includes.</div>"""
            
                replacements.append(self.content[index:close+1])
            
                index = find('${', close)
        
        @web.core.cache.cache('page.content', expires=86400)
        def cache(name, date):
            # TODO: Make this plugin-able.
            content = self.content
            
            if self.engine == 'textile':
                content = textile.Textile().textile(content, html_type='html')
            
            if replacements:
                from web.extras.contentment.components.asset.model import Asset
                
                for replacement in replacements:
                    path, _, args = replacement[2:-1].partition(' ')
                    embedded = Asset.objects(path=path).first()
                    
                    if not embedded:
                        content = content.replace(replacement, u"""<span class="error">Error looking up embedded asset with path <tt>%s</tt>.</span>""" % (path, ))
                    
                    # TODO: There has to be a better way to do this that accounts for quoted strings.
                    args = dict([(i.split('=')[0], i.split('=')[1]) for i in args.split()])
                    
                    try:
                        # embedded = u'''<div class="embed" id="%s-embed">%s</div>''' % (embedded.name, unicode(embedded.embed(**args)))
                        content = content.replace(replacement, unicode(embedded.embed(**args)))
                    
                    except:
                        log.exception("Error while embedding.")
                        content = content.replace(replacement, u"""<span class="error">Error embedding asset with path <tt>%s</tt>.</span>""" % (path, ))
            
            return content
        
        return cache(self.path, self.modified if self.modified else self.created)
    
    @property
    def _content(self):
        """A HTML-stripped version of the rendered content for indexing."""
        
        if self.engine in ('raw', 'mako'):
            return ''
        
        from HTMLParser import HTMLParser
        
        class Stripper(HTMLParser):
            def __init__(self):
                self.reset()
                self.fed = []
            
            def handle_data(self, d):
                self.fed.append(d)
            
            def get_data(self):
                return ''.join(self.fed)
        
        s = Stripper()
        s.feed(self.rendered)
        
        return s.get_data()
    
    def embed(self):
        return self.rendered
