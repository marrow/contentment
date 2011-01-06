## encoding: utf-8
<%inherit file="${context.get('root').properties['org-contentment-theme']}.templates.master"/>

<%def name="title()">Creating new ${kind}</%def>

<header>
    <h1>${title()}</h1>
    <menu class="tabs">\
    % for group in form.children:
<li${' class="active"' if group.name == 'general' else ''}><a href="#${group.name}-set">${group.title}</a></li>\
    % endfor
</menu>
</header>

<section>
    ${unicode(form(data)) | n}
</section>
