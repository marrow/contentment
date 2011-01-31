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


def iter_templates():
    from web.extras.contentment.components.asset.model import Asset
    
    container = Asset.objects(path='/settings/templates/custom').first()
    assert container
    
    yield ':none', "No Template"
    yield '', "Default Template"
    
    custom = Asset.objects(parent=container).order_by('title')
    
    if len(custom):
        yield "Custom Templates", [(template.path, template.title) for template in custom]


def fields(asset):
    root = asset.path == '/'
    
    return [
            ('general', "General", [
                    TextField('title', "Title", title="Appears in window titles, breadcrumb navigation, and directory listings.", required=True),
                    TextArea('description', "Description", title="Plain text description which appears in listings.", rows=3)
                ]),
            
            ('properties', "Properties", [
                    TextField(
                            'name', "Name",
                            title = "The web site root has no name, and as such, the name can not be modified." if root else "When creating a new asset, the name will be generated from the title if missing.",
                            disabled = True if root else None,
                            placeholder = "Web Site Root" if root else None,
                            required = None if root else True
                        ),
                    TagField('tags', "Keywords / Tags", class_="tags", title="Used for searches, both live and saved."), # TODO: tag parsing
                    SelectField('owner', "Author / Owner", values=iter_owners, transform=AssetPathTransform()), # TODO: Path-based asset conversion.
                    SelectField('default', "Default View", values=partial(iter_views, asset)), # TODO
                    SelectField('template', "View Template", title="View templates wrap the content in custom code.", values=iter_templates),
                    DateTimeField('created', "Creation Date", title="The date the asset was created, in UTC."), # TODO: date conversion
                    DateTimeField('modified', "Modification Date", title="The date the asset was last modified, in UTC.")
                ]),
            ('security', "Security", [
                    # FieldSet('access', "Access Control", DefinitionListLayout, [
                    #         Label('acl.about', "Control who has access to this asset and its children."),
                    #         CheckboxField('acl.private', "Private Asset", title="Prevent access to this resource by anyone other than the owner."),
                    #         CheckboxField('acl.member', "Members Only", title="Allow anyone with an account access."),
                    #     ]),
                    FieldSet('publication', "Publication Dates", DefinitionListLayout, [
                            Label('acl.about', "Define the dates between which this asset and its children will be made available."),
                            DateTimeField('acl.publish', "Publication Date", title="Become available after a specific date."),
                            DateTimeField('acl.retract', "Retraction Date", title="Become unavailable after a specific date.")
                        ]),
                    # FieldSet('password', "Password Protection", DefinitionListLayout, [
                    #         Label('acl.about', "Allow access to this asset and its children after password entry."),
                    #         TextField('acl.password', "Password", title="A shared password for accessing this asset and its children."),
                    #     ]),
                ])
        ]
