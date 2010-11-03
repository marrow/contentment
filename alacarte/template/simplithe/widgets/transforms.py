# encoding: utf-8

import datetime

from marrow.util.convert import KeywordProcessor


__all__ = ['TransformException', 'Transform', 'BaseTransform', 'ListTransform', 'TagsTransform', 'IntegerTransform']



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
        value = super(ListTransform).native(value)
        if value is None: return value
        
        return self.processor(value)


class TagsTransform(ListTransform):
    processor = KeywordProcessor(' \t,', normalize=lambda s: s.lower().strip('"'), sort=True, result=list)


class IntegerTransform(Transform):
    def __call__(self, value):
        if value is None: return u''
        
        return unicode(value)
    
    def native(self, value):
        value = value.strip()
        if not value: return None
        
        return int(value)


# 1582-10-15T00:00Z


class DateTimeTransform(Transform):
    base = datetime.datetime
    format = "1582-10-15T00:00Z"
    
    def __call__(self, value):
        pass
    
    def native(self, value):
        pass