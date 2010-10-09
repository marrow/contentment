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
            #contents th, #contents td { text-align: left; padding: 10px; border-bottom: 1px solid #444; }
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
                            <td class="name"><a href="${child.path}/view:contents" title="This is a ${child.__class__.__name__} asset.">${child.name}</a></td>
                            <td class="title"><a href="${child.path}/">${child.title}</a></td>
%     if child.owner:
                            <td class="owner"><a href="${child.owner.path}/">${child.owner.title}</a></td>
%     else:
                            <td class="owner"><em title="No owner set; anonymous, system, or automated asset.">Anonymous</em></td>
%     endif
%     if not child.modified or child.modified == child.created:
                            <td class="date"><time class="created" datetime="${child.created.isoformat()}" title="Creation date.">${child.created.strftime('%B %e, %G at %H:%M:%S')}</time></td>
%     else:
                            <td class="date"><time class="modified" datetime="${child.modified.isoformat()}" title="Modification date.">${child.modified.strftime('%B %e, %G at %H:%M:%S')}</time></td>
%     endif
                            <td class="actions">
                                <a href="${child.path}/action:modify">Modify</a>
                            </td>
                        </tr>
% endfor
                    </tbody>
                </table>
            </div>
        </div>
    </body>
</html>