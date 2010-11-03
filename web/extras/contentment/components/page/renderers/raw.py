# encoding: utf-8

from web.extras.contentment.components.page.api import Renderer


__all__ = ['RawRenderer']



class RawRenderer(Renderer):
    def __call__(self, content):
        return super(RawRenderer, self).__call__(content)
    
    def editor(self, content):
        raise NotImplementedError
