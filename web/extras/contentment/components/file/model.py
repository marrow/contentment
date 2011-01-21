# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""


import mimetypes
from cStringIO import StringIO

import web.core

import mongoengine as db

from web.extras.contentment.components.asset.model import Asset
from widgets import fields


log = __import__('logging').getLogger(__name__)
__all__ = ['File']



class File(Asset):
    _widgets = fields
    _indexable = ['extracted']
    
    default = db.StringField(default="view:preview", max_length=128)
    
    indexed = db.BooleanField(default=True)
    filename = db.StringField(max_length=250)
    mimetype = db.StringField(max_length=250)
    size = db.IntField()
    
    backend = db.StringField(max_length=128, default="gridfs")
    
    content = db.FileField()
    
    @property
    def extracted(self):
        if not self.indexed or self.size > (40*1024*1024):
            return ''
        
        top, _, bottom = self.mimetype.partition('/')
        format = self._component.mimetypes.get(top, dict()).get(bottom, None)
        
        if format and self.indexed:
            content = StringIO(self.content.read())
            return format.index(content)
        
        return ''
    
    @property
    def format(self):
        top, _, bottom = self.mimetype.partition('/')
        
        return self._component.mimetypes.get(top, dict()).get(bottom, None)
    
    def delete(self, *args, **kw):
        if self.content: self.content.delete()
        super(File, self).delete(*args, **kw)
    
    def process(self, formdata):
        formdata = super(File, self).process(formdata)
        
        if formdata.get('content', None) is None:
            try:
                del formdata['content']
            except:
                pass
            return formdata
        
        var = formdata.get('content', None)
        mimetype, encoding = mimetypes.guess_type(var.filename)
        
        del formdata['content']
        
        if self.content:
            self.content.delete()
        
        self.content = var.file
        self.content.content_type = formdata['mimetype'] = mimetype
        self.content.filename = formdata['filename'] = var.filename
        
        formdata['size'] = self.content.get().length
        
        top, _, bottom = formdata['mimetype'].partition('/')
        format = self._component.mimetypes.get(top, dict()).get(bottom, None)
        
        return formdata
    
    def reindex(self, dirty=None):
        super(File, self).reindex(dirty)
    
    def embed(self, **kw):
        return self.format.embed(self, **kw)
