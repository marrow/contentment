## encoding: utf-8
<%inherit file="${context.get('root').properties['org-contentment-theme']}.templates.master"/>
<%namespace file="web.extras.contentment.themes.default.templates.date" name="date"/>

<%def name="title()">Contents of ${asset.__class__.__name__}: ${asset.title}</%def>

<header>
    <h1>${title()}</h1>
</header>

<section id="contents">
<table>
    <thead>
        <tr>
            <th class="handle"></th>
            <th class="name">Name</th>
            <th class="detail">Asset Title</th>
            <th class="owner">Owner</th>
            <th class="date">Created / Modified</th>
            <th class="actions">Actions</th>
        </tr>
    </thead>
    
    <tbody>
<% skipped = 0 %>
% if not asset.children:
        <tr><td colspan="6" style="text-align: center; padding: 2em;"><em>Asset has no child nodes.</em></td></tr>
% endif
% for child in asset.children:
<% if not child.controller.allowed: skipped += 1; continue %>
        <tr id="${child.id}">
            <td class="handle">&#x2af6;&#x2af6;</td>
            <td class="name"><a href="${child.path}/view:contents" title="View the contents of this ${child.__class__.__name__} asset.">${child.name}</a></td>
            <td class="title"><a href="${child.path}/" title="View the default view of this ${child.__class__.__name__} asset.">${child.title}</a></td>
%     if child.owner:
            <td class="owner"><a href="${child.owner.path}/">${child.owner.title}</a></td>
%     else:
            <td class="owner"><em title="No owner set; anonymous, system, or automated asset.">Anonymous</em></td>
%     endif
%     if not child.modified or child.modified == child.created:
            <td class="date">${date.render(child.created, cls='created')}</td>
%     else:
            <td class="date">${date.render(child.created, cls='modified')}</td>
%     endif
            <td class="actions">
% for action in asset.controller.actions:
<%    if action.name == 'create': continue %>
%     if action.authorized(child):
                <a href="${child.path}/action:${action.name}" title="${action.description}">${action.title}</a>
%     endif
% endfor
            </td>
        </tr>
% endfor
    </tbody>
</table>
</section>

<% count = len(asset.children) - skipped %>
<div class="byline tc">Contains <b>${count}</b> Asset${'s' if count != 1 else ''}</div>