<%inherit file="web.extras.contentment.themes.default.master"/>

<%def name="title()">Modifying ${asset.title}</%def>

<form method="post" class="modify">
    <h1>${title()}</h1>
    
    <dl>
        <dt><label for="asset-title">Title</label></dt>
        <dd><input type="text" id="asset-title" name="title" value="${asset.title}"></dd>
        
        <dt><label for="asset-description">Description</label></dt>
        <dd><textarea id="asset-description" name="description">${asset.description or ''}</textarea></dd>
        
% if asset.__class__.__name__ == 'Page':
        <dt>
            <label for="asset-content">Content</label>
            <a style="float: right;" href="http://redcloth.org/hobix.com/textile/">Textile Reference</a>
        </dt>
        <dd><textarea id="asset-content" name="content">${asset.content or ''}</textarea></dd>
% endif
        
        <dt><label for="asset-tags">Tags</label></dt>
        <dd><input type="text" id="asset-tags" name="keywords" value="${' '.join(asset.tags)}"></dd>
        
% if asset.__class__.__name__ == 'Page':
        <dt><label for="asset-template">Page Template</label></dt>
        <dd><select id="asset-template" name="template">
            <option>Default Template</option>
            <optgroup label="Custom Templates">
            </optgroup>
        </select></dd>
% endif
    </dl>
    
    <input type="submit" value="Save Asset"> <input type="button" value="Cancel">
</form>