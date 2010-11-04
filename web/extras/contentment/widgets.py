# encoding: utf-8

from alacarte.template.simplithe import html5 as tag
from alacarte.template.simplithe.widgets import *
from alacarte.template.simplithe.widgets.transforms import *


__all__ = ['ContentmentFooter', 'TagField', 'AssetPathTransform', 'AssetListTransform']



class ContentmentFooter(NestedWidget):
    def __init__(self, name_, title_=None, children=None, referrer=None, *args, **kw):
        self.referrer = referrer
        super(ContentmentFooter, self).__init__(name_, title_, children, *args, **kw)
    
    @property
    def template(self):
        return tag.menu ( id = self.name + '-footer', class_ = "buttons footer" ) [
                [ tag.li ( class_ = "current" ) [ tag.input ( type = 'submit', value = self.title ) ] ] +
                ([ tag.li [ tag.a ( href = self.referrer ) [ "Cancel" ] ] ] if self.referrer else []) +
                ([ tag.div ( class_ = "fr" ) [ tag.li [ [ child(self.data) for child in self.children ] ] ] ] if self.children else [])
            ]


class TagField(TextField):
    transform = TagsTransform()


class AssetPathTransform(BaseTransform):
    def __call__(self, value):
        if not value: return u''
        
        return value.path
    
    def native(self, value):
        from web.extras.contentment.components.asset.model import Asset
        
        value = super(AssetList, self).native(value)
        if value is None: return None
        
        return Asset.objects(path=value).first()


class AssetListTransform(BaseTransform):
    def __call__(self, value):
        if not value: return u''
        
        return u", ".join([i.path for i in value])
    
    def native(self, value):
        from web.extras.contentment.components.asset.model import Asset
        
        value = super(AssetList, self).native(value)
        if value is None: return []
        
        result = []
        
        try:
            for i in value.split(','):
                i = i.strip()
                result.append(Asset.objects(path=i).first())
        
        except:
            log.exception("Error.")
            raise TransformException()
        
        return result
