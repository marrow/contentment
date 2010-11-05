# encoding: utf-8

from alacarte.template.simplithe.widgets import *
from alacarte.template.simplithe.widgets.transforms import BooleanTransform


__all__ = ['fields']



def fields(asset):
    return [
            ('general', "General", [
                    FileField('content', "File Upload"),
                ])
        ]
