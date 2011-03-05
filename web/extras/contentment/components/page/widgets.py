# encoding: utf-8

from alacarte.template.simplithe.widgets import *
from web.extras.contentment.widgets import AssetListTransform


__all__ = ['fields']



def fields(asset):
    return [
            ('general', "General", [
                    TextArea('content', "Content", rows=15),
                    TextField('related', "Related Assets", title="A comma-separated list of asset paths.", transform=AssetListTransform())
                ]),
        
            ('properties', "Properties", [
                    SelectField('engine', "Rendering Engine", title="Text pre-processor.", values=[
                            ('Basic Engines', [
                                    ('textile', "Textile Text-to-HTML"),
                                    ('html', "Sanitized HTML"),
                                ]),
                            ('Advanced Engines', [
                                    ('raw', "Raw (No Processing)"),
                                    ('mako', "Mako Page Template (Insecure)"),
                                    ('css', "CSS Source"),
                                    ('ccss', "Clever CSS Source"),
                                    ('js', "JavaScript Source"),
                                ])
                        ])
                ])
        ]
