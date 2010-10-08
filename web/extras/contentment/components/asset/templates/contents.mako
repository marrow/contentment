<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <!-- <py:if test="'master' in cmf">
        <xi:include py:if="not isinstance(cmf.master, list)" href="cmf.master}" />
        <xi:include py:if="isinstance(cmf.master, list)" py:for="master in cmf.master" href="master}" />
    </py:if> -->
    
    <head>
        <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
        
        <title>Contents of ${asset.title}</title>
        
        <style type="text/css" media="screen">
            
            #contents { width: 100%; border-collapse: collapse; line-height: 100%; }
            #contents th, #contents td { padding: 10px; border-bottom: 1px solid #444; }
            #contents th { padding-top: 0; border-bottom: 1px solid #999; }
            #contents .actions { text-align: right; padding-right: 0; }
            #contents td.actions { padding: 0; }
            
        </style>
    </head>
    
    <body>
        <div class="yui-b">
            <h2>Contents of ${asset.title}</h2>
            
            <div class="content">
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
% for child in asset.children:
                        <tr id="${child.id}">
                            <td class="name"><a href="${child.path}/view:contents" title="This is a %{child.__class__.__name__} asset.">${child.name}</a></td>
                            <!-- <td class="title"><a py:attrs="{'href': child.path + '/'}" py:content="child.title" /></td>
                            <td py:if="child.owner"><a py:attrs="{'href': child.owner.path + '/'}" py:content="child.owner.title">Joe Random Hacker</a></td>
                            <td py:if="not child.owner"><i>Anonymous</i></td>
                            <td class="date" py:if="not child.modified or child.modified == child.created"><abbr class="date" py:attrs="{'title': child.created.isoformat()}" py:content="child.created.strftime(asset.properties['cmf.formats:date'])" /></td>
                            <td class="date" py:if="child.modified and child.modified != child.created"><abbr class="date" py:attrs="{'title': child.modified.isoformat()}" py:content="child.modified.strftime(asset.properties['cmf.formats:date'])" /></td>
                            <td class="actions">
                                <a py:for="url, action in controller.actions" href="${child.path + '/action:' + url}"><img src="/static/img/actions/${action.icon}.png" /></a>
                            </td> -->
                        </tr>
% endfor
                    </tbody>
                </table>
            </div>
        </div>
    </body>
</html>