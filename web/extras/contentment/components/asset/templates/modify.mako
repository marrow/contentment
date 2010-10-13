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
        
        <dt><label for="asset-description">Description</label></dt>
        <dd><textarea id="asset-description" name="description" style="height: 2.5em; width: 98%; display: block;">${asset.description or ''}</textarea></dd>
        
% if asset.__class__.__name__ == 'Page':
        <dt>
            <label for="asset-content">Content</label>
        </dt>
        <dd><textarea id="asset-content" name="content" style="width: 98%; display: block;">${asset.content or ''}</textarea></dd>
% endif
        
        <dt><label for="asset-tags">Tags</label></dt>
        <dd><input type="text" id="asset-tags" name="keywords" value="${' '.join(asset.tags)}" style="width: 98%;"></dd>
        
% if asset.__class__.__name__ == 'Page':
        <dt><label for="asset-template">Page Template</label></dt>
        <dd><select id="asset-template" name="template">
            <option>Default Template</option>
            <optgroup label="Custom Templates">
            </optgroup>
        </select></dd>
% endif
    </dl>
    
    <dl id="properties">
        asdf
    </dl>
    
    <menu class="buttons">
        <li class="current"><input type="submit" value="Save"></li>
        <li><a href="${asset.path if asset.parent.default != asset.name else asset.parent.path}">Cancel</a></li>
        <div class="fr">
            <li><a href="">Textile Reference</a></li>
        </div>
    </menu>
</form>