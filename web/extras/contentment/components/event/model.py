# encoding: utf-8

"""Event model."""

import mongoengine as db

from web.extras.contentment.components.page.model import Page


log = __import__('logging').getLogger(__name__)
__all__ = ['EventContact', 'Event']



class EventContact(db.EmbeddedDocument):
    name = db.StringField(max_length=250)
    email = db.StringField(max_length=250)
    phone = db.StringField(max_length=64)


class Event(Page):
    organizer = db.StringField(max_length=250)
    location = db.StringField(max_length=250)
    starts = db.DateTimeField()
    stops = db.DateTimeField()
    allday = db.BooleanField(default=False)
    contact = db.EmbeddedDocumentField(EventContact)
