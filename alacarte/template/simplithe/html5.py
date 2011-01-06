# encoding: utf-8

from alacarte.template.simplithe import Tag, Flush


__all__ = ['comment', 'html', 'flush']


_doctype = '<!DOCTYPE HTML>\n'
_tags = ['a', 'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'base', 'bdo', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'cite', 'code', 'col', 'colgroup', 'command', 'datalist', 'dd', 'del', 'details', 'dfn', 'div', 'dl', 'dt', 'em', 'embed', 'eventsource', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hgroup', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'keygen', 'label', 'legend', 'li', 'link', 'mark', 'map', 'menu', 'meta', 'meter', 'nav', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'pre', 'progress', 'q', 'ruby', 'rp', 'rt', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strong', 'style', 'sub', 'summary', 'sup', 'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'ul', 'var', 'video', 'wbr']
_partial = ['area', 'base', 'br', 'embed', 'eventsource', 'hr', 'img', 'input', 'link', 'meta', 'param', 'wbr']
_nowrap = ['title', 'textarea', 'pre', 'label', 'option', 'a', 'legend']
_comment = (u'<!--', u'-->')

_attributes = ['accesskey', 'class', 'contenteditable', 'contextmenu', 'dir', 'draggable', 'hidden', 'id', 'lang', 'spellcheck', 'style', 'tabindex', 'title']
_events = ['onabort', 'onblur', 'oncanplay', 'oncanplaythrough', 'onchange', 'onclick', 'oncontextmenu', 'ondblclick', 'ondrag', 'ondragend', 'ondragenter', 'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'ondurationchange', 'onemptied', 'onended', 'onerror', 'onfocus', 'onformchange', 'onforminput', 'oninput', 'oninvalid', 'onkeydown', 'onkeypress', 'onkeyup', 'onload', 'onloadeddata', 'onloadedmetadata', 'onloadstart', 'onmousedown', 'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousewheel', 'onpause', 'onplay', 'onplaying', 'onprogress', 'onratechange', 'onreadystatechange', 'onscroll', 'onseeked', 'onseeking', 'onselect', 'onshow', 'onstalled', 'onsubmit', 'onsuspend', 'ontimeupdate', 'onvolumechange', 'onwaiting']


flush = Flush()


class comment(Tag):
    def enter(self):
        yield _comment[0]

    def exit(self):
        yield _comment[1]

comment = comment()


html = Tag('html', prefix=_doctype)


_locals = locals()

for t in _tags:
    if t not in _locals:
        _locals[t] = Tag(t, simple=t in _partial, indent=not t in _nowrap)
        __all__.append(t)

del _locals

if __name__ == '__main__':
    from timeit import Timer
    
    page = html [
            head [ title [ 'Welcome!' ] ],
            flush, # allow the browser to start downloading static resources early
            body ( class_ = "nav-home" ) [
                    p [
                            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
                        ],
                    flush, # pretend that this next div takes a long time to generate
                    div [ 'foo' ]
                ]
        ]
    
    table_ = [dict(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)] * 1000
    def bigtable(table_): return table (indent=False) [ [(tr [ [(td [ str(i) ]) for i in row.values()] ]) for row in table_ ] ]
    
    print repr(page)
    print
    print [i for i in page.render('ascii')]
    print
    print unicode(page)
    
    # n = 100000
    # duration = Timer("[i for i in page.render('ascii')]", "from __main__ import page").timeit(n)
    # timeper = duration / float(n) * 1000
    # genper = float(n) / duration
    # 
    # print "Timeit (Stream): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)
    # 
    # duration = Timer("unicode(page)", "from __main__ import page").timeit(n)
    # timeper = duration / float(n) * 1000
    # genper = float(n) / duration
    # 
    # print "Timeit (Monolithic): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)
    
    n = 10
    duration = Timer("[i for i in table__.render('ascii')]", "from __main__ import bigtable, table_; table__ = bigtable(table_)").timeit(n)
    timeper = duration / float(n) * 1000
    genper = float(n) / duration
    
    print "Timeit (Bigtable Stream): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)
    
    n = 10
    duration = Timer("unicode(table__).encode('ascii')", "from __main__ import bigtable, table_; table__ = bigtable(table_)").timeit(n)
    timeper = duration / float(n) * 1000
    genper = float(n) / duration
    
    print "Timeit (Bigtable Monolithic): %0.2fs for %d gens: %0.2f usec/gen (%d gen/sec)." % (duration, n, timeper, genper)
