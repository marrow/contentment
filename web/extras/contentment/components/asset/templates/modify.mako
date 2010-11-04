<%inherit file="${context.get('root').properties['org-contentment-theme']}.templates.master"/>

<%def name="title()">Modifying ${asset.__class__.__name__}: ${asset.title}</%def>

<%
    from alacarte.template.simplithe.widgets import Link
    
    form = asset._form(
            None,
            submit="Save",
            referrer=asset.path if getattr(asset.parent, 'default', None) != asset.name else asset.parent.path
        )
    
    form.footer.children.append(Link('textile', "Textile Reference", class_='button', target='_blank', href="http://redcloth.org/hobix.com/textile/"))
%>

<menu class="tabs">
    <h1>${title()}</h1>
% for group in form.children:
    <li${' class="active"' if group.name == 'general' else ''}><a href="#${group.name}-set">${group.title}</a></li>
% endfor
</menu>

${unicode(form(data)) | n}
