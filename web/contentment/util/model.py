# encoding: utf-8

from mongoengine import DynamicEmbeddedDocument
from mongoengine.signals import pre_save_post_validation

from . import utcnow
from .templates import properties


def signal(event):
	def decorator(fn):
		def signal_inner(cls):
			event.connect(fn, sender=cls)
			return cls
		
		fn.signal = signal_inner
		return fn
		
	return decorator


@signal(pre_save_post_validation)
def update_modified_timestamp(sender, document, **kw):
	document.modified = utcnow()


class Properties(DynamicEmbeddedDocument):
	def __repr__(self):
		return repr({f: getattr(self, f) for f in self._dynamic_fields})
	
	def get(self, name, default=None):
		if name not in self: return default
		return getattr(self, name)

	@classmethod
	def __xml_importer__(cls, element):
		if not element.text or not element.text.strip():
			return cls(**element.attrib)

		from marrow.package.loader import load

		return cls(**{element.get('name'): load(element.get('type'))(element.text)})

	__xml__ = properties

