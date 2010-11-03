# encoding: utf-8

from alacarte.template.simplithe.widgets import *
from web.extras.contentment.widgets import AssetListTransform


__all__ = ['fields']


def iter_templates():
    from web.extras.contentment.components.asset.model import Asset
    
    container = Asset.objects(path='/settings/templates/custom').first()
    assert container
    
    yield None, "Default Template"
    
    custom = Asset.objects(parent=container).order_by('title')
    
    if len(custom):
        yield "Custom Templates", [(template.path, template.title) for template in custom]


def fields(asset):
    return [
            ('general', "General", [
                    TextArea('content', "Content", rows=15),
                    TextField('related', "Related Assets", title="A comma-separated list of asset paths.", transform=AssetListTransform())
                ]),
        
            ('properties', "Properties", [
                    SelectField('template', "Page Template", title="Page templates wrap the content in custom code.", values=iter_templates),
                    SelectField('engine', "Rendering Engine", title="Text pre-processor.", values=[
                            ('Basic Engines', [
                                    ('textile', "Textile Text-to-HTML"),
                                    ('html', "Sanitized HTML"),
                                ]),
                            ('Advanced Engines', [
                                    ('raw', "Raw (No Processing)"),
                                    ('mako', "Mako Page Template (Insecure)")
                                ])
                        ])
                ])
        ]
