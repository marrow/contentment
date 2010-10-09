# encoding: utf-8

"""Basic asset controller.

Handles low-level common tasks such as creation, deletion, modification form display, and navigation.
"""

import re

import web

from hashlib import sha256
from datetime import datetime

from web.core import request, session, http
from web.utils.string import normalize
from web.utils.object import yield_property

from marrow.util.convert import tags

# from web.extras.contentment.core import components, action, view
from web.extras.contentment.components.core import BaseController
# from web.extras.contentment.components.asset.core import CoreMethods


log = __import__('logging').getLogger(__name__)
__all__ = ['AssetController']



class AssetController(BaseController):
    """The base controller that all other controllers descend from.
    
    Provides core methods (creation/deletion) and AJAX APIs."""
    
    def __init__(self, identifier=None):
        super(AssetController, self).__init__(identifier)
        
        # self.api_core = CoreMethods(self)
    
    def _template(self, name, data=None, base=None):
        from web.extras.contentment.components.asset.model import Asset
        
        if data is None:
            data = dict()
        
        data['asset'] = self.asset
        data['root'] = Asset.objects(path='/').first()
        
        if base is None:
            base = '.'.join(self.__module__.split('.')[:-1])
        
        log.warn(self.__module__)
        
        return (
                'mako:' + base + '.templates.' + name,
                data
            )
    
    def view_default(self):
        return self.view_contents()
    
    # @view("Contents") # TODO: Roll above code into @view/action decorator.
    def view_contents(self, sort=None):
        return self._template('contents', base='.'.join(AssetController.__module__.split('.')[:-1]))
    
    # @action("Create") # TODO: Make this a RESTful method for GET/POST.
    def action_create(self, **kw):
        return self._template('create', base='.'.join(AssetController.__module__.split('.')[:-1]))
    
    # @action("Modify") # TODO: As per Create.
    def action_modify(self, **kw):
        asset = self.asset
        
        if not kw:
            return self._template('modify', base='.'.join(AssetController.__module__.split('.')[:-1]))
        
        if 'submit' in kw: del kw['submit']
        
        if 'tags' in kw:
            kw['tags'] = tags(kw['tags'])
        
        for i, j in kw.iteritems():
            setattr(asset, i, j)
        
        asset.modified = datetime.now()
        
        asset.save()
        
        raise http.HTTPFound(location=asset.path + '/')
        
        return self._template('modify', base='.'.join(AssetController.__module__.split('.')[:-1]))
    
    # @action("Remove")
    def action_remove(self, key=None, force=False):
        """Delete this asset and all descendants."""
        
        # TODO: Hash the last modification date and path and verify against `key`.
        # TODO: Allow overriding of the key check using the `force` value.
        # TODO: If `key` not present, display 
        
        parent_path = self.asset.parent.path
        
        self.asset.delete()
        
        raise web.core.http.HTTPFound(location=parent_path)
        
        return self._template('remove', base='.'.join(AssetController.__module__.split('.')[:-1]))


# TODO: Remove old code.
'''
    OLD CODE

    @action("Create", icon='base-create')
    def action_create(self, **kw):
        """Create new assets."""
        
        from itertools import groupby
        
        component = None
        for i in components.itervalues():
            if isinstance(self, i.controller):
                component = i
                break
        if not component: log.error("Unable to find component for %r!", self)
        
        tmp = [(j.group, i, j) for i, j in components.iteritems()]
        tmp.sort()
        
        kinds = []
        for k, g in groupby(tmp, lambda i: i[0]):
            kinds.append((k, [(i, j) for x, i, j in g if j.authorized(self.asset) and component.authorize(j)]))
        
        
        return ('genshi:web.extras.cmf.components.asset.views.create',
                dict(kinds=kinds))
    
    # TODO Rewrite this to use Sprox.
    def _action_create(self, **kw):
        # if 'cmf.authentication.account' not in session:
            # flash("You do not have sufficient priveledges to create assets here.", 'error')
            # session['cmf.authentication.target.asset'] = self.asset.guid
            # session['cmf.authentication.target'] = self.asset.path_info
            # session.save()
            # redirect('/action:authenticate')
        
        if 'name' in kw:
            from cmf.components.asset.model import session as DBSession, Tag
            
            try:
                if 'name' not in kw or not kw['name']:
                    kw['name'] = normalize(kw['title'], yield_property(self.asset.children, 'name'))
                else: kw['name'] = normalize(kw['name'], yield_property(self.asset.children, 'name'))
                
                log.debug("Creating asset of kind %r: %r", components[kw['kind']], kw)
                
                kw['owner_guid'] = session['cmf.authentication.account'].id
                
                tags = None
                if 'tags' in kw:
                    tags = kw['tags']
                    del kw['tags']
                
                asset = components[kw['kind']].constructor(**kw)
                
                self.asset.attach(asset, after=kw['direction'] == 'after')
                
                if tags:
                    asset.tags.extend(Tag.split(tags))
            
            except:
                DBSession.rollback()
                log.exception("Error creating asset.")
            
            else:
                DBSession.commit()
                redirect(asset.path + '/action:modify')
        
        
        log.debug("Kinds: %r", kinds)
        
        return ('genshi:web.extras.cmf.components.asset.views.create',
                dict(kinds=kinds))
    
    
    @action("Remove", icon='base-delete')
    def _action_remove(self):
        """Delete this asset and all descendants."""
        
        parent = self.asset.parent
        l, r = self.asset.l, self.asset.r
        self.asset.delete()
        model.session.commit()
        model.Asset.stargate(model.Asset.l > l, model.Asset.r > r, -(r - l + 1))
        
        flash("success::Successfully Deleted Asset::Succesfully removed asset.")
        redirect(url(parent.path + '/'))
    
    # TODO Rewrite this to use Sprox.
    @action("Properties", icon='base-properties')
    def _action_properties(self, **kw):
        """Modify behind-the-scenes information about the asset."""
        
        from cmf.components.asset.model import Tag
        from elixir import session as DBSession
        
        if 'name' in kw:
            self.asset.modified = datetime.now()
            
            for i, j in kw.iteritems():
                if i in ['name', 'default']:
                    setattr(self.asset, i, j)
                
                elif i == 'tags':
                    del self.asset.tags[:]
                    self.asset.tags.extend(Tag.split(kw['tags']))
                
                elif i in ['published', 'retracted']:
                    try:
                        from tw.forms.validators import DateTimeConverter
                        setattr(self.asset, i, DateTimeConverter().to_python(j.strip()) if j.strip() else None)
                        
                    except:
                        log.exception("Invalid date given, date dropped.")
                        pass
            
            DBSession.commit()
            
            flash("Changes made successfully.", 'success')
            redirect(self.asset.path + '/')
        
        return ('genshi:cmf.components.asset.views.properties',
                dict())
    
    
    # TODO
    @action("Security", icon='base-security')
    def _action_security(self, **kw):
        """Modify permissions and other security settings for this asset."""
        
        if kw.get('action', None) == "save":
            if kw.get('guest', False):
                if kw.get('password', None):
                    self.asset.properties['cmf.authentication.guestpass'] = md5.md5(kw['password']).hexdigest()
                    flash("success::Saved Changes::Successfully updated guest pass.")
            
            elif 'cmf.authentication.guestpass' in self.asset.properties:
                del self.asset.properties['cmf.authentication.guestpass']
                flash("success::Saved Changes::Successfully removed guest pass.")
            
            model.session.commit()
            
            redirect(self.asset.path + '/')
        
        return ('genshi:cmf.components.asset.views.security',
                dict())
    
'''