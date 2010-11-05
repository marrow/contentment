<%inherit file="${context.get('root').properties['org-contentment-theme']}.templates.master"/>

<%def name="title()">Creating new ${kind}</%def>

<menu class="tabs">
    <h1>${title()}</h1>
% for group in form.children:
    <li${' class="active"' if group.name == 'general' else ''}><a href="#${group.name}-set">${group.title}</a></li>
% endfor
</menu>

${unicode(form(data)) | n}
