# encoding: utf-8

from alacarte.template.simplithe import html5 as tag
from alacarte.template.simplithe.widgets import transforms as t

from base import Input, BooleanInput


__all__ = ['TextField', 'HiddenField', 'SearchField', 'URLField', 'PhoneField', 'EmailField', 'PasswordField', 'DateTimeField', 'DateField', 'MonthField', 'WeekField', 'TimeField', 'DateTimeLocalField', 'NumberField', 'FloatField', 'RangeField', 'FloatRangeField', 'ColorField', 'FileField', 'RadioField', 'CheckboxField', 'TextArea', 'SelectField']



class TextField(Input):
    type_ = 'text'


class HiddenField(Input):
    type_ = 'hidden'


class SearchField(Input):
    type_ = 'search'


class URLField(Input):
    type_ = 'url'


class PhoneField(Input):
    type_ = 'tel'


class EmailField(Input):
    type_ = 'email'


class PasswordField(Input):
    type_ = 'password'


class DateTimeField(Input):
    transform = t.DateTimeTransform()
    type_ = 'datetime'


class DateField(Input):
    # transform = t.URLTransform()
    type_ = 'date'


class MonthField(Input):
    # transform = t.URLTransform()
    type_ = 'month'


class WeekField(Input):
    # transform = t.URLTransform()
    type_ = 'week'


class TimeField(Input):
    # transform = t.URLTransform()
    type_ = 'time'


class DateTimeLocalField(Input):
    # transform = t.URLTransform()
    type_ = 'datetimelocal'


class NumberField(Input):
    transform = t.IntegerTransform()
    type_ = 'number'


class FloatField(NumberField):
    transform = t.FloatTransform()


class RangeField(Input):
    transform = t.IntegerTransform()
    type_ = 'range'


class FloatRangeField(RangeField):
    transform = t.FloatTransform()


class ColorField(Input):
    type_ = 'color'


class FileField(Input):
    type_ = 'file'


class RadioField(BooleanInput):
    type_ = 'radio'


class CheckboxField(BooleanInput):
    type_ = 'checkbox'


class TextArea(Input):
    @property
    def template(self):
        return tag.textarea (
                name = self.name,
                id = self.name + '-field',
                **self.args
            ) [ self.value ]


class SelectField(Input):
    def __init__(self, name_, title_=None, values=None, *args, **kw):
        super(SelectField, self).__init__(name_, title_, *args, **kw)
        self.values = values
    
    @property
    def template(self):
        value = self.value
        values = self.values() if hasattr(self.values, '__call__') else self.values
        options = []
        
        for option in values:
            if not isinstance(option[1], list):
                options.append(tag.option ( value = option[0], selected = option[0] == value ) [ option[1] ])
                continue
            
            options.append(tag.optgroup ( label = option[0] ) [[
                    tag.option ( value_ = i[0], selected = i[0] == value ) [ i[1] ]
                for i in option[1] ]])
        
        return tag.select (
                name = self.name,
                **self.args
            ) [ options ]
