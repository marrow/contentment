<%inherit file="${context.get('root').properties['org-contentment-theme']}.templates.master"/>

<%def name="title()">ACL for ${asset.__class__.__name__}: ${asset.title}</%def>

<% acl = [i for i in asset.acl_] %>

<h1 class="primary">${title()}</h1>

<div id="contents">
<table>
    <thead>
        <tr>
            <th class="handle"></th>
            <th class="name">Rule Owner</th>
            <th class="detail">Asset Title</th>
        </tr>
    </thead>
    
    <tbody>
% if not acl:
        <tr><td colspan="6" style="text-align: center; padding: 2em;"><em>Asset has no ACL.</em></td></tr>
% endif
% for owner, rule in acl:
        <tr>
            <td class="handle">&#x2af6;&#x2af6;</td>
            <td class="name"><a href="${owner.path}/view:acl" title="View the acl of this ${owner.__class__.__name__} asset.">${owner.name}</a></td>
            <td class="detal">${rule}</td>
        </tr>
% endfor
    </tbody>
</table>
</div>

<div class="byline tc">Contains <b>${len(acl)}</b> ACL Rule${'s' if len(acl) != 1 else ''}</div>