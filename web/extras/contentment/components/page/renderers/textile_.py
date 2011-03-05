# encoding: utf-8

import textile

from web.extras.contentment.components.page.api import Renderer


__all__ = ['TextileRenderer']



class Textile(textile.Textile):
    btag = ('bq', 'bc', 'notextile', 'pre', 'h[1-6]', 'fn\d+', 'p', 'div')
    btag_lite = ('bq', 'bc', 'p', 'div')


class TextileRenderer(Renderer):
    def __call__(self, content):
        return super(TextileRenderer, self).__call__(Textile().textile(content, html_type='html'))
    
    def editor(self, content):
        raise NotImplementedError
