# encoding: utf-8

from api import FileFormat

from alacarte.template.simplithe import html5 as tag


__all__ = ['ImageFileFormat']



class ImageFileFormat(FileFormat):
    mimetypes = {'image': '*'}
    
    def embed(self, asset, width=None, height=None):
        return tag.img (
                src = asset.path + '/view:download/' + asset.filename,
                width = width,
                height = height
            )
