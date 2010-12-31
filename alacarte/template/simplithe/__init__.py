# encoding: utf-8

from sys import getcheckinterval, setcheckinterval
from copy import copy, deepcopy


__all__ = ['Fragment', 'Tag', 'Text', 'AutoTag', 'tag']



class NoDefault(object):
    pass


def quoteattrs(context, attrs):
    """Escape and quote a dict of attribute/value pairs.
    
    Escape &, <, and > in a string of data, then quote it for use as
    an attribute value.  The " character will be escaped as well.
    Also filter out None values.
    """
    for a, v in attrs.items():
        if v is None or v is NoDefault:
            continue
        
        if callable(v):
            v = v(context)
        
        if isinstance(v, bool):
            if v:
                yield ' ' + a.strip(u'_')
            
            continue
        
        if not isinstance(v, unicode):
            v = unicode(v)
        
        yield ' '  + a.strip(u'_') + '="'
        
        for s, r in [(u'&', u"&amp;"), (u">", u"&gt;"), (u"<", u"&lt;"), (u'"', u"&quot;")]:
            try:
                v = v.replace(s, r)
            
            except AttributeError:
                raise AttributeError('Argument %s of %r can not be quoted.' % (a, context))
        
        yield v + '"'


def escape(v):
    """Escape &, <, and > in a string of data."""
    for s, r in [(u'&', u"&amp;"), (u">", u"&gt;"), (u"<", u"&lt;")]:
        v = v.replace(s, r)
    
    return v


class Fragment(object):
    def __init__(self, data_=None, *args, **kw):
        self.args = list(args)
        self.attrs = kw
        self.data = data_
        
        super(Fragment, self).__init__()
    
    def __repr__(self):
        return "<%s args=%r attrs=%r>" % (self.name, self.args, self.attrs)
    
    def clear(self):
        self.args = list()
        self.attrs = dict()


class Tag(Fragment):
    prefix = None
    simple = False
    strip = False
    indent = True
    
    def __init__(self, name=NoDefault, prefix=NoDefault, simple=NoDefault, strip=NoDefault, indent=NoDefault, *args, **kw):
        self.name = self.__class__.__name__ if name is NoDefault else name
        self.children = []
        self.args = list(args)
        self.attrs = kw
        self.data = None
        
        if prefix is not NoDefault: self.prefix = prefix
        if simple is not NoDefault: self.simple = simple
        if strip is not NoDefault: self.strip = strip
        if indent is not NoDefault: self.indent = indent
        
        super(Tag, self).__init__(*args, **kw)
    
    def __call__(self, data_=None, strip=NoDefault, *args, **kw):
        self = deepcopy(self)
        
        self.data = data_
        if strip is not NoDefault: self.strip = strip
        self.args.extend(list(args))
        self.attrs.update(kw)
        
        return self
    
    def __getitem__(self, k):
        if not k: return self
        
        self = deepcopy(self)
        
        if not isinstance(k, (tuple, list)):
            k = [k]
        
        for fragment in k:
            if isinstance(fragment, basestring):
                self.children.append(escape(fragment))
                continue
        
            self.children.append(fragment)
        
        return self
    
    def __repr__(self):
        return "<%s children=%d args=%r attrs=%r>" % (self.name, len(self.children), self.args, self.attrs)
    
    def __unicode__(self):
        """Return a serialized version of this tree/branch."""
        
        ci = getcheckinterval()
        setcheckinterval(0)
        
        value = u''.join(self.render())
        
        setcheckinterval(ci)
        return value
    
    def enter(self):
        if self.strip:
            raise StopIteration()
            
        if self.prefix:
            yield self.prefix
        
        yield u'<' + self.name
        
        for attr in quoteattrs(self, self.attrs):
            yield attr
        
        yield u'>'
    
    def exit(self):
        if self.simple or self.strip:
            raise StopIteration()
            
        yield u'</' + self.name + u'>'
    
    def render(self, encoding=None):
        indentation = 0
        text = False
        stack = []
        buf = u""
        
        for k, t in self:
            if k == 'enter':
                indent = getattr(t, 'indent', True)
                
                stack.append(t)
                if t.strip: continue
                
                if text and indent:
                    buf += u'\n'
                
                buf += u'    ' * indentation
                
                for element in t.enter():
                    buf += element
                
                if indent: buf += u'\n'
                
                indentation += 1
                text = False
                continue
            
            if k == 'exit':
                indent = getattr(t, 'indent', True)
                
                stack.pop()
                if t.strip: continue
                
                indentation -= 1
                
                if not t.simple:
                    if text and indent: buf += u'\n'
                    if indent: buf += u'    ' * indentation
                
                for element in t.exit():
                    buf += element
                
                if not t.simple or t.children: buf += u'\n'
                text = False
                continue
            
            if k == 'text':
                indent = getattr(stack[-1], 'indent', True)
                
                if not text and indent:
                    buf += u'    ' * indentation
                    
                buf += t.replace(u'\n', u'\n' + u'    ' * indentation) if indent else t
                text = True
            
            if k == 'flush':
                yield buf.encode(encoding) if encoding else buf
                buf = ""
        
        yield buf.encode(encoding) if encoding else buf
    
    def __copy__(self):
        t = Tag(self.name, *self.args, **deepcopy(self.attrs))
        t.data = self.data
        t.children = self.children
        return t
    
    def __iter__(self):
        yield 'enter', self
        
        for child in self.children:
            if isinstance(child, Fragment):
                for element in child:
                    yield element
                continue
            
            if hasattr(child, '__call__'):
                value = child(self)
                
                if isinstance(value, basestring):
                    yield 'text', unicode(value)
                    # yield 'text', u'\n'
                    continue
                
                for element in child(self):
                    yield element
                
                continue
            
            yield 'text', unicode(child)
            # yield 'text', u'\n'
        
        yield 'exit', self
    
    def clear(self):
        self.children = list()
        super(Tag, self).clear()
    
    def empty(self):
        self.children = list()


class Text(Fragment):
    def __init__(self, data=None, escape=True, *args, **kw):
        self.escape = escape
        
        super(Text, self).__init__(data, *args, **kw)
    
    def __iter__(self):
        yield 'text', escape(unicode(self.data)) if self.escape else unicode(self.data)


class Flush(Fragment):
    def __iter__(self):
        yield 'flush', None
