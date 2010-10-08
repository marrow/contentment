# encoding: utf-8

"""

Asset controller core JSON API methods.

"""

from datetime               import datetime

import                                          web
from web.core                                   import Controller, request, session, http
from web.extras                                 import cmf



log = __import__('logging').getLogger(__name__)
__all__ = ['CoreMethods']



class TagMethods(Controller):
    __trailing_slash__ = False # we want .../tags to appear as a method by itself.  No trailing slash on index for us.
    
    def __init__(self, controller):
        self.controller = controller
    
    def index(self, hidden=False, format='json'):
        if format not in ['json', 'bencode']: return "Infalid format requested."
        
        return format, dict(status="ok", message="Retreived tag list.", tags=[i for i in self.controller.asset.tags if hidden or ':' not in i])

    def add(self, tag=None, format='json'):
        if tag is None: return "You must define a tag to add."
        if format not in ['json', 'bencode']: return "Infalid format requested."
        
        try:
            if tag in self.controller.asset.tags: return dict(status="warn", message="Tag already present.")
            self.controller.asset.tags.append(tag)
            cmf.components.asset.model.session.commit()
            return format, dict(status="ok", message="Added tag.", tag=tag)

        except:
            log.exception("Error adding tag.")
            cmf.components.asset.model.session.rollback()

        return format, dict(status="error", message="Unable to add tag.")

    def remove(self, tag=None, format='json'):
        if tag is None: return "You must define a tag to remove."
        if format not in ['json', 'bencode']: return "Infalid format requested."
        
        try:
            if tag not in self.controller.asset.tags: return dict(status="error", message="Tag not present.")
            self.controller.asset.tags.remove(tag)
            cmf.components.asset.model.session.commit()
            return format, dict(status="ok", message="Removed tag.", tag=tag)

        except:
            log.exception("Error adding tag.")
            cmf.components.asset.model.session.rollback()

        return format, dict(status="error", message="Unable to remove tag.")




class CoreMethods(Controller):
    def __init__(self, controller):
        self.controller = controller
        self.tags = TagMethods(controller)
    
    def sort(self, index, **kw):
        import model
        
        index = int(index)
        
        try:
            children = self.controller.asset.parent.children.all()
            oldIndex = children.index(self.controller.asset)
            
            log.debug("Parent's children: %r", children)
            log.debug("Old index: %d  New index: %d", oldIndex, index)
            
            if index == oldIndex:
                return dict(status="warning", message="Asset should not be moved.  Did you click the handle instead of dragging it?")
            
            if index == 0:
                log.debug("Moving %r to top of child list.", self.controller.asset)
                self.controller.asset.parent.attach(self.asset, after=False, below=True)
            
            elif index == len(children) - 1:
                log.debug("Moving %r to bottom of child list.", self.controller.asset)
                self.controller.asset.parent.attach(self.asset, after=True, below=True)
            
            else:
                log.debug("Moving %r above %r.", self.controller.asset, children[index if index < oldIndex else index + 1])
                children[index if index < oldIndex else index + 1].attach(self.controller.asset, after=False, below=False)
            
        except:
            model.session.rollback()
            log.exception("Unable to move %r", self.controller.asset)
            return dict(status="error", message="Unable to move this asset.  Reload this page and try again.")
        
        model.session.commit()
        return dict(status="ok", message="Asset successfully moved.")
    
    
    def property(self, name, value=None, format='json'):
        # TODO: Security check.  Ensure the user attempting to set the property has the rights to do so.
        if format not in ['json', 'bencode']: return "Infalid format requested."
        
        try:
            if value:
                setattr(self.controller.asset, name, value)
                cmf.components.asset.model.session.commit()
                return format, dict(status="ok", message="Successfully updated property.", name=name, result=value)
            
            else:
                return format, dict(status="ok", message="Successfully retrieved property.", name=name, value=getattr(self.controller.asset, name))
        
        except:
            log.exception("Error updating property.")
            cmf.components.asset.model.session.rollback()
        
        return dict(status="error", message="Unable to update property.")
