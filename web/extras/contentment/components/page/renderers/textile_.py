# encoding: utf-8

import textile

from web.extras.contentment.components.page.api import Renderer


__all__ = ['TextileRenderer']



class TextileRenderer(Renderer):
    def __call__(self, content):
        return super(RawRenderer, self).__call__(textile.Textile().textile(content, html_type='html'))
    
    def editor(self, content):
        raise NotImplementedError
