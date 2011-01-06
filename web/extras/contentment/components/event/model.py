# encoding: utf-8

"""Event model."""

import mongoengine as db

from web.extras.contentment.components.page.model import Page
from widgets import fields


log = __import__('logging').getLogger(__name__)
__all__ = ['EventContact', 'Event']



class EventContact(db.EmbeddedDocument):
    name = db.StringField(max_length=250)
    email = db.StringField(max_length=250)
    phone = db.StringField(max_length=64)


class Event(Page):
    _widgets = fields
    
    default = db.StringField(default="view:event", max_length=128)
    
    organizer = db.StringField(max_length=250)
    location = db.StringField(max_length=250)
    starts = db.DateTimeField()
    stops = db.DateTimeField()
    allday = db.BooleanField(default=False)
    contact = db.EmbeddedDocumentField(EventContact)
    
    def process(self, formdata):
        formdata = super(Event, self).process(formdata)
        
        contact = EventContact()
        
        for field in 'name', 'email', 'phone':
            combined = 'contact.' + field
            if combined in formdata:
                setattr(contact, field, formdata[combined])
                del formdata[combined]
        
        formdata['contact'] = contact
        
        return formdata
    
