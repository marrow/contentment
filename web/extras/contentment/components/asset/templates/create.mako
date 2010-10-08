<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" xmlns:xi="http://www.w3.org/2001/XInclude">
    <py:if test="'master' in cmf">
        <xi:include py:if="not isinstance(cmf.master, list)" href="${cmf.master}" />
        <xi:include py:if="isinstance(cmf.master, list)" py:for="master in cmf.master" href="${master}" />
    </py:if>
    
    <head>
        <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
        
        <title>Create a new Asset</title>
    </head>
    
    <body>
        <div class="yui-b">
            <h2>Create a new Asset</h2>
            
            <div class="content">
                <form id="form" method="post" class="serial">
                    <div class="yui-g">
                        <div class="yui-u first field required">
                            <label for="">Asset Type</label>
                            <div class="help">What kind of asset would you like to create?</div>
                            <select name="kind" style="width: 100%;">
                                <option disabled="true">Please select an asset type.</option>
                                <optgroup py:for="group, options in kinds" py:if="options" py:attrs="{'label': group if group else 'Unknown Types'}">
                                    <option py:for="value, option in options" py:attrs="{'value': value}" py:content="option.title + ((': ' + option.summary) if option.summary else '')" />
                                </optgroup>
                            </select>
                        </div>
                        
                        <div class="yui-u field">
                            <label for="">Attachment</label>
                            <div class="help">At what position would you like to create this asset?</div>
                            <select name="direction">
                                <option value="before">Before any siblings.</option>
                                <option value="after" selected="True">After any siblings.</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="yui-g">
                        <div class="yui-u first field optional">
                            <label for="">Asset Name</label>
                            <div class="help">The container-unique name for the asset. May only contain letters, numbers, and hyphens.</div>
                            <input type="text" name="name" />
                        </div>
                        
                        <div class="yui-u field required">
                            <label for="title-editor">Title</label>
                            <div class="help">Enter the display title of this asset. This is displayed at the top of the document, in lists, and in searches.</div>
                            <input type="text" id="title-editor" class="textarea" name="title" />
                        </div>
                    </div>
                    
                    <div class="field optional">
                        <label for="description-editor">Description</label>
                        <div class="help">The description is used in list views and searches, but can appear at the top of views in a distinct style.</div>
                        <textarea rows="3" cols="25" class="textarea" id="description-editor" name="description"></textarea>
                    </div>
                    
                    <div class="field optional">
                        <label for="tags">Tags</label>
                        <div class="help">Tags (keywords) associated with this asset.</div>
                        <input type="text" name="tags" />
                    </div>
                    
                    <div class="yui-g">
                        <div class="yui-u first field optional">
                            <label for="tags">Publication Date</label>
                            <div class="help">This asset will become accessible after this date and time.</div>
                            <input type="text" name="published" />
                        </div>
                        
                        <div class="yui-u field optional">
                            <label for="tags">Retraction Date</label>
                            <div class="help">This asset will cease being available after this date and time.</div>
                            <input type="text" name="retracted" />
                        </div>
                    </div>
                    <div class="help">Dates must be entered in <i>YYYY/MM/DD HH:MM</i> 24-hour format.</div>
                    
                    <div class="footer">
                        <ul class="actions buttons right">
                            <li><button type="submit" class="button positive icon submit">Create Asset</button></li
                            ><li><a class="button negative icon close" py:attrs="{'href': asset.path + '/'}" onclick="return confirm('Are you sure?  Any unsaved changes will be lost.');">Cancel</a></li>
                        </ul>
                        <div style="clear: both;"><!-- IE --></div>
                    </div>
                </form>
            </div>
        </div>
    </body>
</html>