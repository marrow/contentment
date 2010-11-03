# encoding: utf-8

from functools import partial

from alacarte.template.simplithe.widgets import *
from web.extras.contentment.widgets import TagField, AssetPathTransform


__all__ = ['fields']


def iter_owners():
    from web.extras.contentment.components.identity.model import Identity
    
    yield None, "Anonymous"
    
    yield "Identities", [(identity.path, "%s (%s)" % (identity.name, identity.title)) for identity in Identity.objects.order_by('title')]


excluded_actions = ['delete']

def iter_views(asset):
    controller = asset.controller
    
    yield "Actions", [(action.name_, action.title) for action in controller.actions if action.name not in excluded_actions]
    
    yield "Views", [(view.name_, view.title) for view in controller.views]
    
    if asset.children:
        yield "Children", [(child.name, child.title) for child in asset.children]


def fields(asset):
    root = asset.path == '/'
    
    return [
            ('general', "General", [
                    TextField('title', "Title", title="Appears in window titles, breadcrumb navigation, and directory listings."),
                    TextArea('description', "Description", title="Plain text description which appears in listings.", rows=3)
                ]),
        
            ('properties', "Properties", [
                    TextField(
                            'name', "Name",
                            title = "The web site root has no name, and as such, the name can not be modified." if root else "Modify this to re-name the asset.",
                            disabled = True if root else None,
                            placeholder = "Web Site Root" if root else None
                        ),
                    TagField('tags', "Keywords / Tags", class_="tags", title="Used for searches, both live and saved."), # TODO: tag parsing
                    SelectField('owner', "Author / Owner", values=iter_owners, transform=AssetPathTransform()), # TODO: Path-based asset conversion.
                    SelectField('default', "Default View", values=partial(iter_views, asset)), # TODO
                    DateTimeField('created', "Creation Date", title="The date the asset was created, in UTC."), # TODO: date conversion
                    DateTimeField('modified', "Modification Date", title="The date the asset was last modified, in UTC.")
                ]),
        ]
