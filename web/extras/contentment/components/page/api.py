# encoding: utf-8


__all__ = ['Renderer']


class Renderer(object):
    replacements = True
    
    def __call__(self, content):
        # TODO: Substitutions.
        
        return content
    
    def editor(self, content):
        raise NotImplementedError
