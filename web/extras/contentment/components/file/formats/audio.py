# encoding: utf-8

from api import FileFormat

from alacarte.template.simplithe import html5 as tag


__all__ = ['AudioFileFormat']



class AudioFileFormat(FileFormat):
    mimetypes = {'audio': ['mpeg', 'ogg', 'vorbis', 'x-wav', 'mp4a', 'mp4a-latm']}
    
    def embed(self, asset, preload=True, autoplay=False, loop=False, controls=True):
        path = asset.path + '/view:download/' + asset.filename + "?inline=True"
        
        return tag.audio (
                preload = preload,
                autobuffer = preload,
                autoplay = autoplay,
                loop = loop,
                controls = controls
            ) [
                tag.source ( src = path )
            ]