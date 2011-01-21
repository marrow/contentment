# encoding: utf-8

import datetime

from pytz import utc

from marrow.util.convert import KeywordProcessor


__all__ = ['TransformException', 'Transform', 'BaseTransform', 'ListTransform', 'TagsTransform', 'IntegerTransform', 'FloatTransform', 'DateTimeTransform']



class TransformException(Exception):
    pass


class Transform(object):
    def __call__(self, value):
        """Convert a value from Python to Web-safe.
        
        Override this in your subclass.
        """
        
        raise NotImplementedError
    
    def native(self, value):
        """Convert a Web-safe value to Python.
        
        Override this in your subclass.
        """
        
        raise NotImplementedError


class BaseTransform(Transform):
    def __call__(self, value):
        if value is None: return u''
        
        try:
            return unicode(value)
        
        except:
            raise TransformException()
    
    def native(self, value):
        if value == '': return None
        
        if isinstance(value, str):
            return value.decode('utf-8')
        
        return value


class ListTransform(BaseTransform):
    processor = KeywordProcessor(', \t\n', normalize=lambda s: s.strip('"'))
    
    def __init__(self, processor=None):
        if processor is not None: self.processor = processor
    
    def __call__(self, value):
        if value is None: return u''
        
        if not isinstance(value, list):
            raise TransformException()
        
        return unicode(self.processor(value))
    
    def native(self, value):
        value = super(ListTransform, self).native(value)
        if value is None: return value
        
        return self.processor(value)


class TagsTransform(ListTransform):
    processor = KeywordProcessor(' \t,', normalize=lambda s: s.lower().strip('"'), sort=True, result=list)


class BooleanTransform(Transform):
    def __call__(self, value):
        if value: return 'True'
        return None
    
    def native(self, value):
        if not value: return False
        return True


class IntegerTransform(Transform):
    def __call__(self, value):
        if value is None: return u''
        
        return unicode(value)
    
    def native(self, value):
        value = value.strip()
        if not value: return None
        
        return int(value)


class FloatTransform(Transform):
    def __call__(self, value):
        if value is None: return u''
        
        return unicode(value)
    
    def native(self, value):
        value = value.strip()
        if not value: return None
        
        return float(value)


class DateTimeTransform(Transform):
    base = datetime.datetime
    format = "%Y-%m-%d %H:%M:%S"
    
    def __call__(self, value):
        if value is None: return u''
        
        return unicode(value.strftime(self.format))
    
    def native(self, value):
        value = value.strip()
        if not value: return None
        
        value = self.base.strptime(value, self.format)
        
        return value if value.tzinfo is not None else value.replace(tzinfo=utc)
