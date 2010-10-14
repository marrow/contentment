<%inherit file="${context.get('root').properties['org-contentment-theme']}.templates.master"/>

<%def name="title()">Modifying ${asset.__class__.__name__}: ${asset.title}</%def>

<form method="post" class="modify">
    <menu class="buttons top">
        <li class="current"><input type="submit" value="Save"></li>
        <li><a href="${asset.path if asset.parent.default != asset.name else asset.parent.path}">Cancel</a></li>
        <div class="fr">
            <li><a href="">Textile Reference</a></li>
        </div>
    </menu>
    
    <h1>${title()}</h1>
    
    <dl id="general">
        <div style="float: left; width: 33%;">
            <dt><label for="asset-name">Name</label></dt>
            <dd><input type="text" id="asset-name" name="name" value="${asset.name}" style="width: 100%;">
        </div>
        <div style="float: left; width: 63%; padding-left: 3%;">
            <dt><label for="asset-title">Title</label></dt>
            <dd><input type="text" id="asset-title" name="title" value="${asset.title}" style="width: 100%;"></dd>
        </div>
        
        <dt><label for="asset-tags">Keywords / Tags</label></dt>
        <dd><input type="text" id="asset-tags" name="keywords" value="${' '.join(asset.tags)}" style="width: 98%;"></dd>
        
        <dt><label for="asset-description">Description</label></dt>
        <dd><textarea id="asset-description" name="description" style="height: 2.5em; width: 98%; display: block;">${asset.description or ''}</textarea></dd>
        
% if asset.controller._modify_form:
<%include file="${context.get('asset').controller._modify_form}"/>
% endif
    </dl>
    
    <menu class="buttons">
        <li class="current"><input type="submit" value="Save"></li>
        <li><a href="${asset.path if asset.parent.default != asset.name else asset.parent.path}">Cancel</a></li>
        <div class="fr">
            <li><a href="">Textile Reference</a></li>
        </div>
    </menu>
</form>