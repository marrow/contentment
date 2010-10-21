<%inherit file="${context.get('root').properties['org-contentment-theme']}.templates.master"/>

<%def name="title()">Modifying ${asset.__class__.__name__}: ${asset.title}</%def>

<form method="post" class="modify">
    <menu class="tabs">
        <h1>${title()}</h1>
        <li class="active"><a href="#tab-general">General</a></li>
        <li><a href="#tab-properties">Properties</a></li>
        <li><a href="#tab-security">Security</a></li>
    </menu>
    
    <dl id="tab-general">
        <dt><label for="asset-title">Title</label></dt>
        <dd><input type="text" id="asset-title" name="title" value="${asset.title}" style="width: 98%;"></dd>
        
        <dt><label for="asset-tags">Keywords / Tags</label></dt>
        <dd><input type="text" id="asset-tags" name="keywords" value="${' '.join(asset.tags)}" style="width: 98%;"></dd>
        
        <dt><label for="asset-description">Description</label></dt>
        <dd><textarea id="asset-description" name="description" style="height: 2.5em; width: 98%; display: block;">${asset.description or ''}</textarea></dd>
        
% if asset.controller._modify_form:
<%include file="${context.get('asset').controller._modify_form}"/>
% endif
    </dl>
    
    <dl id="tab-properties">
        <dt><label for="asset-name">Name</label></dt>
        <dd><input type="text" id="asset-name" name="name" value="${asset.name}" style="width: 100%;">
    </dl>
    
    <menu class="buttons footer">
        <li class="current"><input type="submit" value="Save"></li>
        <li><a href="${asset.path if asset.parent.default != asset.name else asset.parent.path}">Cancel</a></li>
        <div class="fr">
            <li><a target="_blank" href="http://redcloth.org/hobix.com/textile/">Textile Reference</a></li>
        </div>
    </menu>
</form>