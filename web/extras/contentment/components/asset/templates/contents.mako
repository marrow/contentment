<%inherit file="${context.get('root').properties['org-contentment-theme']}.templates.master"/>

<%def name="title()">Contents of ${asset.title}</%def>        
        
<style type="text/css" media="screen">
    
    #contents { width: 100%; border-collapse: collapse; line-height: 100%; }
    #contents th, #contents td { text-align: left; padding: 10px; border-bottom: 1px solid #444; }
    #contents th { padding-top: 0; border-bottom: 1px solid #999; }
    #contents .actions { text-align: right; padding-right: 0; }
    #contents td.actions { padding: 0; }
    
</style>

<h1>Contents of ${asset.title}</h1>

<table id="contents">
    <thead>
        <tr>
            <th class="name">Name</th>
            <th class="detail">Asset Title</th>
            <th class="owner">Owner</th>
            <th class="date">Created / Modified</th>
            <th class="actions">Actions</th>
        </tr>
    </thead>
    
    <tbody>
% if not asset.children:
        <tr><td colspan="5" style="text-align: center; padding: 2em;"><em>Asset has no child nodes.</em></td></tr>
% endif
% for child in asset.children:
        <tr id="${child.id}">
            <td class="name"><a href="${child.path}/view:contents" title="This is a ${child.__class__.__name__} asset.">${child.name}</a></td>
            <td class="title"><a href="${child.path}/">${child.title}</a></td>
%     if child.owner:
            <td class="owner"><a href="${child.owner.path}/">${child.owner.title}</a></td>
%     else:
            <td class="owner"><em title="No owner set; anonymous, system, or automated asset.">Anonymous</em></td>
%     endif
%     if not child.modified or child.modified == child.created:
            <td class="date"><time class="created" datetime="${child.created.isoformat()}" title="Creation date.">${child.created.strftime(root.properties['org-contentment-formats-date'])}</time></td>
%     else:
            <td class="date"><time class="modified" datetime="${child.modified.isoformat()}" title="Modification date.">${child.modified.strftime(root.properties['org-contentment-formats-date'])}</time></td>
%     endif
            <td class="actions">
                <a href="${child.path}/action:modify">Modify</a>
            </td>
        </tr>
% endfor
    </tbody>
</table>