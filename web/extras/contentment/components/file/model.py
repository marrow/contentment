# encoding: utf-8

"""Asset model.

All asset types must descend from this class.
"""


import mimetypes

import web.core

import mongoengine as db

from web.extras.contentment.components.asset.model import Asset
from widgets import fields


log = __import__('logging').getLogger(__name__)
__all__ = ['File']



class File(Asset):
    _widgets = fields
    
    default = db.StringField(default="view:preview", max_length=128)
    
    filename = db.StringField(max_length=250)
    mimetype = db.StringField(max_length=250)
    size = db.IntField()
    
    content = db.FileField()
    
    def delete(self, *args, **kw):
        if self.content: self.content.delete()
        super(File, self).delete(*args, **kw)
    
    def process(self, formdata):
        # web.core.request.POST['content']
        
        if formdata.get('content', None) is None:
            return formdata
        
        var = formdata.get('content', None)
        mimetype, encoding = mimetypes.guess_type(var.filename)
        
        del formdata['content']
        
        if self.content:
            self.content.replace(var.file, content_type=mimetype, filename=var.filename)
        
        else:
            self.content.put(var.file, content_type=mimetype, filename=var.filename)
        
        formdata['filename'] = var.filename
        formdata['mimetype'] = mimetype
        formdata['size'] = self.content.length
        
        return formdata
