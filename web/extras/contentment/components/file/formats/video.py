# encoding: utf-8

from api import FileFormat

from alacarte.template.simplithe import html5 as tag


__all__ = ['VideoFileFormat']



class VideoFileFormat(FileFormat):
    mimetypes = {'video': ['mpeg', 'mp4', 'quicktime', 'ogg']}
    
    def embed(self, asset, preload=True, autoplay=False, loop=False, controls=True, width=None, height=None, poster=None):
        path = asset.path + '/view:download/' + asset.filename + "?inline=True"
        
        return tag.video (
                preload = preload,
                autobuffer = preload,
                autoplay = autoplay,
                loop = loop,
                controls = controls,
                width = width,
                height = height,
                poster = poster
            ) [
                tag.source ( src = path )
            ]
