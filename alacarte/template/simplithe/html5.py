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
    page = html [
            head [ title [ 'Welcome!'] ],
            body ( class_ = "nav-home" ) [
                    p [ 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' ],
                    flush,
                    div ( 'foo' )
                ]
        ]
    
    print repr(page)
    print
    print [i for i in page.render('ascii')]
    print
    print "\n", unicode(page)
