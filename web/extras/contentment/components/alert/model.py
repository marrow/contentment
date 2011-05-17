# encoding: utf-8

"""Event model."""

import mongoengine as db

from web.extras.contentment.components.page.model import Page
from widgets import fields
from alacarte.template.simplithe import html5 as tag


log = __import__('logging').getLogger(__name__)
__all__ = ['Alert']



class Alert(Page):
    _widgets = fields
    
    default = db.StringField(default="view:alert", max_length=128)
    priority = db.StringField(default="information", choices=['check', 'information', 'question', 'warning'], max_length=11)
    
    def embed(self):
        return tag.table ( class_ = "alert-embed alert-" + self.priority, onclick="window.location = '" + self.path "';" ) [
                tag.tr [
                        ([ tag.td ( class_ = "alert-image", rowspan = 2 ) [ tag.Text(self.children[0].embed(), escape=False) ] ] if self.children and hasattr(self.children[0], 'embed') else [ tag.td ( class_ = "alert-image", rowspan = 2 ) [ tag.Text('&nbsp;', escape=False) ] ]) + [
                        tag.th [ self.title ],
                    ]],
                tag.tr [
                        tag.td [ self.description ]
                    ]
            ]
