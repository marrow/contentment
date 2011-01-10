# encoding: utf-8

from alacarte.template.simplithe.widgets import *


__all__ = ['fields']



def fields(asset):
    return [
            ('general', "General", [
                    FileField('content', "File Upload"),
                    CheckboxField('indexed', "Indexed", title="Enable content extraction and indexing."),
                ])
        ]
