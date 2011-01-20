# encoding: utf-8

from mongoengine.document import Document, EmbeddedDocument
from mongoengine import fields as db


class SearchTerm(EmbeddedDocument):
    meta = {'allow_inheritance': False}
    term = db.StringField(db_field='t')
    weight = db.FloatField(db_field='w')


class DocumentIndex(Document):
    meta = {
        'allow_inheritance': False,
        'collection': 'index',
    }
    
    doc_id = db.ObjectIdField('_id')
    terms = db.DictField(default={})
    length = db.IntField(default=0)
