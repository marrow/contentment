# encoding: utf-8


__all__ = ['FileFormat']


class FileFormat(object):
    mimetypes = {}
    
    def index(self, asset):
        return []
    
    def embed(self, asset):
        return ''