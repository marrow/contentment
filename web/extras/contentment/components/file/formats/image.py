# encoding: utf-8

from api import FileFormat

from alacarte.template.simplithe import html5 as tag


__all__ = ['ImageFileFormat']



class ImageFileFormat(FileFormat):
    mimetypes = {'image': ['bmp', 'gif', 'jpeg', 'png', 'tiff']}
    
    def embed(self, asset, width=None, height=None):
        path = asset.path + '/view:download/' + asset.filename + "?inline=True"
        
        return tag.img (
                src = path,
                width = width,
                height = height
            )
