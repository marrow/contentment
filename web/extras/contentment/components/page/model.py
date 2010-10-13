# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""

import re
import web
import textile

import mongoengine as db

from web.extras.contentment.components.asset.model import Asset


log = __import__('logging').getLogger(__name__)
__all__ = ['Page']
__model__ = __all__



class Textile(textile.Textile):
    btag = ('bq', 'bc', 'notextile', 'pre', 'h[1-6]', 'fn\d+', 'p', 'div')
    
    def lists(self, text):
        """
        >>> t = Textile()
        >>> t.lists("* one\\n* two\\n* three")
        '\\t<ul>\\n\\t\\t<li>one</li>\\n\\t\\t<li>two</li>\\n\\t\\t<li>three</li>\\n\\t</ul>'
        """
        pattern = re.compile(r'^([#*@]+%s .*)$(?![^#*@])' % self.c, re.U|re.M|re.S)
        return pattern.sub(self.fList, text)
    
    def fList(self, match):
        text = match.group(0).split("\n")
        result = []
        lists = []
        for i, line in enumerate(text):
            try:
                nextline = text[i+1]
            except IndexError:
                nextline = ''
            
            m = re.search(r"^([#*@]+)(%s%s) (.*)$" % (self.a, self.c), line, re.S)
            if m:
                tl, atts, content = m.groups()
                nl = ''
                nm = re.search(r'^([#*@]+)\s.*', nextline)
                if nm:
                    nl = nm.group(1)
                if tl not in lists:
                    lists.append(tl)
                    atts = self.pba(atts)
                    line = "\t<%s%s>\n\t\t<li>%s" % (self.lT(tl), atts, self.graf(content))
                else:
                    line = "\t\t<li>" + self.graf(content)
                
                if len(nl) <= len(tl):
                    line = line + "</li>"
                for k in reversed(lists):
                    if len(k) > len(nl):
                        line = line + "\n\t</%sl>" % self.lT(k)
                        if len(k) > 1:
                            line = line + "</li>"
                        lists.remove(k)
            
            result.append(line)
        return "\n".join(result)
    
    def lT(self, input):
        if re.search(r'^#+', input):
            return 'ol'
        elif re.search(r'^@', input):
            return 'menu'
        else:
            return 'ul'


class Page(Asset):
    content = db.StringField()
    engine = db.StringField(max_length=250, default="textile")
    template = db.StringField(max_length=250)
    
    @property
    def rendered(self):
        @web.core.cache.cache('page.content', expires=3600)
        def cache(name, date):
            if self.engine == 'textile':
                return Textile().textile(self.content, head_offset=1, html_type='html')
            
            else:
                return self.content
        
        return cache(self.path, self.modified if self.modified else self.created)
