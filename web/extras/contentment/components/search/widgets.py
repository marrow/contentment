# encoding: utf-8

from alacarte.template.simplithe.widgets import *
from web.extras.contentment.widgets import AssetListTransform


__all__ = ['fields']



def fields(asset):
    return [
            ('general', "General", [
                    TextField('query', "Search Query"),
                    # TextField('where', "Limit Search To", default=['/'], title="A comma-separated list of asset paths.", transform=AssetListTransform())
                ]),
        ]
