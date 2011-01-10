# encoding: utf-8

from alacarte.template.simplithe.widgets import SelectField


__all__ = ['fields']



def fields(asset):
    return [
            ('general', "General", [
                    SelectField('priority', "Priority",
                            title = "The priority is used to style the alert when embedded, e.g. to choose an accompanying icon or color scheme.",
                            values = [
                                    ('warning', "Warning"),
                                    ('information', "Informational"),
                                    ('question', "Question Mark"),
                                    ('check', "Check Mark"),
                                ]
                        ),
                ])
        ]
