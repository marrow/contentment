# encoding: utf-8

"""Basic asset controller.

Handles low-level common tasks such as creation, deletion, modification form display, and navigation.
"""

import re

import web.core

from hashlib import sha256
from datetime import datetime

from web.core import request, session, http
from web.utils.string import normalize
from web.utils.object import yield_property

from marrow.util.convert import tags

from web.extras.contentment.api import action, view
from web.extras.contentment.core import components
from web.extras.contentment.components.core import BaseController
from web.extras.contentment.components.asset.core import CoreMethods


log = __import__('logging').getLogger(__name__)
__all__ = ['AssetController']



class AssetController(BaseController):
    """The base controller that all other controllers descend from.
    
    Provides core methods (creation/deletion) and AJAX APIs."""
    
    def __init__(self, identifier=None):
        super(AssetController, self).__init__(identifier)
        
        self.api_core = CoreMethods(self)
    
    @property
    def allowed(self):
        asset = self.asset
        
        method = getattr(self, asset.default.replace(':', '_'), None)
        if not method: return True # TODO
        
        return method.authorized(asset)
    
    @view("ACL", "Display the access control list rules that apply to this asset.")
    def view_acl(self):
        return 'acl', None
    
    @view("Contents", "Display a directory listing showing the contents of this asset.")
    def view_contents(self, sort=None):
        return 'contents', None
    
    def _form(self, asset=None, referrer=None, label="Save"):
        from alacarte.template.simplithe.widgets import Link
        
        if asset is None:
            asset = self.asset
        
        form = asset._form(None, submit=label, referrer=referrer)
        form.footer.children.append(Link('textile', "Textile Reference", class_='button', target='_blank', href="http://redcloth.org/hobix.com/textile/"))
        
        return form
    
    @action("Create", "Create a new asset.")
    def action_create(self, kind=None, **kw):
        from web.extras.contentment.components.asset.model import Asset
        
        if kind is None:
            return ''
        
        asset = [j for i, j in components[kind].model.iteritems() if issubclass(j, Asset)][0]
        asset = asset(owner=web.auth.user.identity)
        form = self._form(asset, web.core.request.referrer, "Create")
        
        if not kw:
            return 'create', dict(kind=asset.__class__.__name__, form=form, data=asset._data)
        
        if 'submit' in kw: del kw['submit']
        
        try:
            result, remaining = form.native(kw)
        
        except:
            if web.core.config.get('debug', False):
                raise
            
            log.exception("Error processing form.")
            web.core.session['flash'] = dict(cls="error", title="Server Error", message="Unable to create asset; see system log for details." % (asset.__class__.__name__, asset.title, asset.path))
            return 'create', dict(kind=asset.__class__.__name__, form=form, data=asset._data)
        
        dirty = []
        
        if 'name' not in result or not result['name']:
            replacement = re.compile('\W+')
            result['name'] = replacement.sub('-', result['title'].lower())
        
        if result.get('tags', None) is None: result['tags'] = []
        
        result = asset.process(result)
        
        for name, value in result.iteritems():
            dirty.append(name)
            setattr(asset, name, value)
        
        try:
            asset.save(dirty=dirty)
        
        except:
            if web.core.config.get('debug', False):
                raise
            
            log.exception('Error creating record.')
            web.core.session['flash'] = dict(cls="error", title="Server Error", message="Unable to create asset; see system log for details." % (asset.__class__.__name__, asset.title, asset.path))
            return 'create', dict(kind=asset.__class__.__name__, form=form, data=asset._data)
        
        asset.attach(self.asset)
        
        web.core.session['flash'] = dict(cls="success", title="Success", message="Successfully created %s \"%s\", located at %s." % (asset.__class__.__name__, asset.title, asset.path))
        
        raise http.HTTPFound(location=asset.path + '/')
    
    @action("Modify", "Modify this asset.")
    def action_modify(self, **kw):
        asset = self.asset
        
        if not kw:
            return 'modify', dict(data=asset._data)
        
        if 'submit' in kw: del kw['submit']
        
        try:
            result, remaining = asset._form(None).native(kw)
        
        except:
            log.exception("Error processing form.")
            return 'modify', dict(data=asset._data)
        
        # Handle special fields.
        
        rename = False
        reindex = False
        dirty = []
        
        # Root node must not be renamed.
        if asset.path == '/': del result['name']
        else: rename = asset.name != result['name']
        
        result['tags'] = sorted(result['tags']) if result['tags'] else []
        
        # Handle explicit setting of the modification time.
        if not result['modified'] or result['modified'] == asset.modified.replace(microsecond=0):
            result['modified'] = datetime.utcnow()
        
        result = asset.process(result)
        
        for field, value in result.iteritems():
            try:
                if getattr(asset, field) == value: continue
            
            except:
                log.exception("Unable to compare two versions of the same attribute!  Marking dirty to be safe.")
            
            dirty.append(field)
            setattr(asset, field, value)
        
        # return repr((dirty, dict([(i, j) for i, j in result.iteritems() if i in dirty])))
        
        asset.save(dirty=dirty)
        
        web.core.session['flash'] = dict(cls="success", title="Success", message="Successfully updated %s \"%s\", located at %s." % (asset.__class__.__name__, asset.title, asset.path))
        
        raise http.HTTPFound(location=asset.path + '/')
    
    @action("Delete", "Delete this asset and all of its descendants.")
    def action_delete(self, key=None, force=False):
        """Delete this asset and all descendants."""
        
        # TODO: Hash the last modification date and path and verify against `key`.
        # TODO: Allow overriding of the key check using the `force` value.
        # TODO: If `key` not present, display 
        
        asset = self.asset
        
        kind = asset.__class__.__name__
        title = asset.title
        path = asset.path
        
        path = asset.path
        parent_path = asset.parent.path
        
        asset.delete()
        
        web.core.session['flash'] = dict(cls="success", title="Success", message="Successfully deleted %s \"%s\", located at %s." % (kind, title, path))
        
        if web.core.request.referrer.startswith(path):
            raise web.core.http.HTTPFound(location=parent_path)
        
        else:
            raise web.core.http.HTTPFound(location=web.core.request.referrer)
        
        return 'remove', None
