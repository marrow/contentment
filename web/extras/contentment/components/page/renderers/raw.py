# encoding: utf-8

from web.extras.contentment.components.page.api import Renderer


__all__ = ['RawRenderer', 'MakoRenderer']



class RawRenderer(Renderer):
    def __call__(self, content):
        return super(RawRenderer, self).__call__(content)
    
    def editor(self, content):
        raise NotImplementedError


class MakoRenderer(RawRenderer):
    def __call__(self, content):
        return "<b>This type of page is not meant to be viewed directly, rather, it will be utilized by the system elsewhere.</b>"
