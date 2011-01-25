# encoding: utf-8

from api import FileFormat

from alacarte.template.simplithe import html5 as tag

from marrow.util.convert import boolean


__all__ = ['AudioFileFormat']



class AudioFileFormat(FileFormat):
    mimetypes = {'audio': ['mpeg', 'ogg', 'vorbis', 'x-wav', 'mp4a', 'mp4a-latm']}
    
    def embed(self, asset, preload=True, autoplay=False, loop=False, controls=True, width=None):
        path = asset.path + '/view:download/' + asset.filename + "?inline=True"
        
        preload = boolean(preload)
        autoplay = boolean(autoplay)
        loop = boolean(loop)
        controls = boolean(controls)
        
        return tag.audio (
                preload = preload,
                autobuffer = preload,
                autoplay = autoplay,
                loop = loop,
                controls = controls,
                width = width,
                src = path
            )