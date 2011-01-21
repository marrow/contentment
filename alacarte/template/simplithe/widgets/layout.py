# encoding: utf-8

from alacarte.template.simplithe import html5 as tag

from base import Layout, Widget, Label


__all__ = ['DefinitionListLayout', 'TableLayout', 'SubmitFooter']



class DefinitionListLayout(Layout):
    @property
    def template(self):
        parts = []
        
        for child in self.children:
            if not isinstance(child, Label):
                parts.append(tag.dt [ self.label(child.name, for_=child)() ])
            
            parts.append(tag.dd [ child(self.data) ])
        
        return tag.dl ( class_ = "layout" ) [ parts ]


class TableLayout(Layout):
    @property
    def template(self):
        return tag.table ( **self.args ) [ [(
                tag.tr [ tag.th [ self.label(child.name, for_=child)() ],
                tag.td [ child(self.data) ] ]
            ) for child in self.children] ]


class SubmitFooter(Widget):
    @property
    def template(self):
        return tag.div ( **self.args ) [
                tag.input ( type = 'submit', name = self.name, value = self.title )
            ]
