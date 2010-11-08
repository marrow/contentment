# encoding: utf-8

from api import FileFormat

from alacarte.template.simplithe import html5 as tag


__all__ = ['PDFFileFormat']



class PDFFileFormat(FileFormat):
    mimetypes = {'application': ['pdf', 'x-pdf']}
    
    def embed(self, asset, width="100%", height=500):
        path = asset.path + '/view:download/' + asset.filename + "?inline=True"
        
        return tag.embed ( src = path, width = width, height = height )
        
        # return tag.object (
        #         clsid = "clsid:D27CDB6E-AE6D-11cf-96B8-444553540000",
        #         type_ = "application/pdf"
        #         width = width,
        #         height = height,
        #         data = path
        #     ) [
        #         tag.param ( name = "src", value = path ),
        #         tag.param ( name = "movie", value = path ),
        #         tag.param ( name = "quality", value = "high" ),
        #         tag.param ( name = "bgcolor", value = "#FFFFFF" ),
        #         tag.embed ( src = path, quality = "high", bgcolor = "#FFFFFF", width = width, height = height, type_ = "pdf" )
        #     ]
        # 
        # 
        #         src = asset.path + '/view:download/' + asset.filename,
        #         width = width,
        #         height = height,
        #         type_ = "application/pdf",
        #         title = asset.title
        #     )
