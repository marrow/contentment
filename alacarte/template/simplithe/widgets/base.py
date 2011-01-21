# encoding: utf-8

from copy import copy, deepcopy

from alacarte.template.simplithe import NoDefault
from alacarte.template.simplithe import html5 as tag

from transforms import BaseTransform, BooleanTransform


__all__ = ['Widget', 'NestedWidget', 'Form', 'FieldSet', 'Label', 'Layout', 'Input', 'BooleanInput', 'Link']



class Widget(object):
    transform = BaseTransform()
    default = None
    
    def __init__(self, name_, title_=None, transform=NoDefault, default=NoDefault, data_=NoDefault, **kw):
        self.name = name_
        self.title = title_
        self.data = dict() if data_ is NoDefault else data_
        self.args = kw
        
        if transform is not NoDefault: self.transform = transform
        if default is not NoDefault: self.default = default
    
    @property
    def value(self):
        value = self.data.get(self.name, self.default)
        return self.transform(value) if self.transform else value
    
    def native(self, data):
        value = data.get(self.name, None)
        
        if value is None:
            return self.default
        
        return self.transform.native(value) if self.transform else value
    
    @property
    def template(self):
        raise NotImplementedError
    
    def __call__(self, data=NoDefault):
        local = copy(self) # Thread Safety
        
        if data is not NoDefault:
            if isinstance(local.data, dict):
                local.data.update(data)
            
            else:
                local.data = data
        
        return local.template


class NestedWidget(Widget):
    def __init__(self, name_, title_=None, children=None, *args, **kw):
        self.children = children if children else list()
        super(NestedWidget, self).__init__(name_, title_, *args, **kw)
    
    def native(self, data):
        result = dict()
        
        for child in self.children:
            if isinstance(child, NestedWidget):
                result.update(child.native(data)[0])
                continue
            
            result[child.name] = child.native(data)
        
        remaining = dict()
        
        for i in data:
            if i not in result:
                remaining[i] = data[i]
        
        return result, remaining


class Form(NestedWidget):
    def __init__(self, name_, title_=None, layout=None, children=[], footer=None, *args, **kw):
        super(Form, self).__init__(name_, title_, children, *args, **kw)
        
        self.layout = layout
        self.footer = footer
        
        if 'method' not in self.args:
            self.args['method'] = 'post'
    
    @property
    def template(self):
        return tag.form ( id = self.name + '-form', **self.args ) [
                ([
                    self.layout(self.name, children=self.children)(self.data)
                ] if self.layout else [
                    child(self.data) for child in self.children
                ]) + ([
                    self.footer(self.name)(self.data) if isinstance(self.footer, type) else self.footer(self.data)
                ] if self.footer else [])
            ]


class FieldSet(NestedWidget):
    def __init__(self, name_, title_=None, layout=None, children=[], *args, **kw):
        super(FieldSet, self).__init__(name_, title_, children, *args, **kw)
        
        self.layout = layout
    
    @property
    def template(self):
        return tag.fieldset (
                id = self.name + '-set',
                **self.args
            ) [
                ([tag.legend [ self.title ] ] if self.title else []) + ([
                    self.layout(self.name, children=self.children)(self.data)
                ] if self.layout else [
                    child(self.data) for child in self.children
                ])
            ]


class Label(Widget):
    def __init__(self, name_, title_=None, for_=None, *args, **kw):
        self.for_ = for_
        super(Label, self).__init__(name_, title_, *args, **kw)
    
    @property
    def template(self):
        return tag.label (
                for_ = (self.for_.name + '-field') if self.for_ else None
            ) [ self.title if self.title else self.for_.title ]


class Layout(NestedWidget):
    label = Label


class Input(Widget):
    type_ = None
    
    @property
    def template(self):
        return tag.input (
                type_ = self.type_,
                name = self.name,
                id = self.name + '-field',
                value = self.value,
                **self.args
            )


class BooleanInput(Input):
    transform = BooleanTransform()
    
    @property
    def template(self):
        return tag.div [[ tag.input (
                    type_ = self.type_,
                    name = self.name,
                    id = self.name + '-field',
                    checked = self.value,
                    **self.args
                )] + [
                    tag.label ( for_ = self.name + '-field' ) [ self.args.get('title') ]
                ] if 'title' in self.args else []]


class Link(Widget):
    @property
    def template(self):
        return tag.a ( id = self.name + "-link", **self.args ) [ self.title ]
