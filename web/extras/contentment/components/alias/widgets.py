# encoding: utf-8

from alacarte.template.simplithe.widgets import *
from alacarte.template.simplithe.widgets.transforms import BooleanTransform


__all__ = ['fields']


'''
detailed = db.BooleanField(default=True)
unique = db.BooleanField(default=False) # track only unique visitors
session = db.BooleanField(default=False) # register this alias in the session for tracking
'''

def fields(asset):
    return [
            ('general', "General", [
                    TextField('target', "Target Address", title="An absolute or complete URL.", required=True),
                    NumberField('hits', "Alias Hits", title="The number of times this Alias has redirected users.", step=1, min=0),
                ]),
            ('properties', "Properties", [
                    CheckboxField('detailed', "Track Detailed Statistics", title="When enabled this alias will track information about those that are redirected."),
                    CheckboxField('unique', "Track Unique Visitors Only", title="When collecting detailed information, only collect information from unique visitors."),
                    CheckboxField('session', "Register Hit in Session", title="Add this alias to the current user's session for referral tracking.")
                ])
        ]
