# encoding: utf-8

from api import FileFormat

from alacarte.template.simplithe import html5 as tag


__all__ = ['AudioFileFormat']



class AudioFileFormat(FileFormat):
    mimetypes = {'audio': ['mpeg']}
    
    def embed(self, asset, preload=True, autoplay=False, loop=False, controls=True):
        return tag.audio (
                preload = preload,
                autobuffer = preload,
                autoplay = autoplay,
                loop = loop,
                controls = controls
            ) [
                tag.source ( src = asset.path + '/view:download/' + asset.filename )
            ]