# encoding: utf-8

import slate

from api import FileFormat

from alacarte.template.simplithe import html5 as tag


__all__ = ['PDFFileFormat']



class PDFFileFormat(FileFormat):
    mimetypes = {'application': ['pdf', 'x-pdf']}
    
    def embed(self, asset, width="100%", height=500):
        path = asset.path + '/view:download/' + asset.filename + "?inline=True"
        download = path = asset.path + '/view:download/' + asset.filename
        
        return tag.embed ( src = path, width = width, height = height, type = "application/pdf" ) [
                tag.p [
                        "If you are unable to view this PDF inline, feel free to ",
                        tag.a ( href = download ) [ "download it" ],
                        "."
                    ]
            ]
    
    def index(self, fh):
        doc = slate.PDF(fh)
        return u' '.join([i.decode('utf8') for i in doc])
        