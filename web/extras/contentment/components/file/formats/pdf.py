# encoding: utf-8

import slate

from api import FileFormat

from alacarte.template.simplithe import html5 as tag


__all__ = ['PDFFileFormat']



class PDFFileFormat(FileFormat):
    mimetypes = {'application': ['pdf', 'x-pdf']}
    
    def embed(self, asset, width="100%", height=500):
        path = asset.path + '/view:download/' + asset.filename + "?inline=True"
        
        return tag.embed ( src = path, width = width, height = height )
    
    def index(self, fh):
        doc = slate.PDF(fh)
        return u' '.join([i.decode('utf8') for i in doc])
        