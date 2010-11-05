# encoding: utf-8

from alacarte.template.simplithe.widgets import *
from alacarte.template.simplithe.widgets.transforms import BooleanTransform


__all__ = ['fields']



def fields(asset):
    return [
            ('details', "Details", [
                    TextField('organizer', "Event Organizer", title="The name of the event organizer, individual or organization."),
                    TextField('location', "Event Location"),
                    DateTimeField('starts', "Event Starts", title="The start date/time of the event.", required=True),
                    DateTimeField('stops', "Event Stops", title="The ending date/time of the event."),
                    CheckboxField('allday', "All Day Event", title="When enabled start and end times will be ignored, only the dates will be used."),
                ]),
            ('contact', "Contact", [
                    TextField('contact.name', "Contact Name"),
                    TextField('contact.email', "Contact E-Mail Address"),
                    TextField('contact.phone', "Contact Phone Number")
                ])
        ]
