# encoding: utf-8

"""Comment model."""

import textile

import mongoengine as db

from web.extras.contentment.components.asset.model import Asset


log = __import__('logging').getLogger(__name__)
__all__ = ['Comment']



class CommentAuthor(db.EmbeddedDocument):
    name = db.StringField(max_length=250)
    email = db.StringField(max_length=250)
    url = db.StringField(max_length=255)


class Comment(Asset):
    default = db.StringField(default="view:comment", max_length=128)
    
    content = db.StringField()
    poster = db.EmbeddedDocumentField(CommentAuthor, default=None)
    
    @property
    def rendered(self):
        @web.core.cache.cache('comment.content', expires=3600)
        def cache(name, date):
            return textile.Textile(restricted=True, lite=False, noimage=False).textile(self.content, html_type='html')
        
        return cache(self.path, self.modified if self.modified else self.created)
