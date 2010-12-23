# encoding: utf-8

import slate

from api import FileFormat

from alacarte.template.simplithe import html5 as tag


__all__ = ['PDFFileFormat']



class HTMLFileFormat(FileFormat):
    mimetypes = {'text': ['html'], 'application': ['xhtml+xml']}
    
    def embed(self, asset, width="100%", height=500):
        path = asset.path + '/view:download/' + asset.filename + "?inline=True"
        
        return tag.iframe ( src = path, width = width, height = height )
    
    def index(self, fh):
        from HTMLParser import HTMLParser
        
        class Stripper(HTMLParser):
            def __init__(self):
                self.reset()
                self.fed = []
            
            def handle_data(self, d):
                self.fed.append(d)
            
            def get_data(self):
                return ''.join(self.fed)
        
        s = Stripper()
        s.feed(fh.read())
        
        return s.get_data()
