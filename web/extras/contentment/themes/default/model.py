# encoding: utf-8

"""Default theme model."""


import mongoengine as db

from web.extras.contentment.components.theme.model import Theme


log = __import__('logging').getLogger(__name__)
__all__ = ['DefaultTheme']
__model__ = __all__



class Paths(db.EmbeddedDocument):
    header = db.StringField(max_length=250, default="/settings/templates/header")
    menu = db.StringField(max_length=250, default="/settings/templates/menu")
    footer = db.StringField(max_length=250, default="/settings/templates/footer")


class DefaultTheme(Theme):
    breadcrumb = db.BooleanField(default=True)
    paths = db.EmbeddedDocumentField(Paths, default=Paths())
