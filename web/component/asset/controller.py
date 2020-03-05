# encoding: utf-8

from webob.exc import HTTPNotFound
from markupsafe import Markup, escape

from .model import Asset

log = __import__('logging').getLogger(__name__)


class AssetController:
	__dispatch__ = 'resource'
	
	def __init__(self, context, document, reference=None):
		self._ctx = context
		self._doc = document
		
		log.info("Loaded asset.", extra=dict(asset=repr(document.id)))
	
	def post(self, kind, name, title):
		if not self._ctx.uid:
			return dict(ok=False, message="Unauthorized.")
		
		from web.component.page.model import Page
		from web.component.page.block.reference import ReferenceBlock
		from web.component.page.block.content import TextBlock
		
		parent = self._doc
		
		if parent.parent.handler == parent.name:
			parent = parent.parent
		
		if kind == 'Page':
			text = '<p>Nullam quis risus eget urna mollis ornare vel eu leo.</p>'
			obj = Page(name=name, title={'en': title, 'fr': title}, content=[
					ReferenceBlock(target=Asset.objects.get(path='/theme/part/header')),
					TextBlock(content={'en': text, 'fr': text}),
					ReferenceBlock(target=Asset.objects.get(path='/theme/part/footer')),
				])
			obj.parents = parent.parents + [parent]
			obj.parent = parent
			obj.path = '/' + (parent.path + '/' + name).lstrip('/')
			obj = obj.save()
			
			return dict(ok=True, location=obj.path)
		
		obj = Asset(name=name, title={'en': title, 'fr': title})
		obj.parents = parent.parents + [parent]
		obj.parent = parent
		obj.path = '/' + (parent.path + '/' + name).lstrip('/')
		obj = obj.save()
		
		return dict(ok=True, location=parent.path)
	
	def delete(self):
		if not self._ctx.uid:
			return dict(ok=False, message="Unauthorized.")
		
		if self._doc.properties.get('immutable', False):
			return dict(ok=False, message="Asset may not be deleted.")

		if self._doc.parent.handler == self._doc.name:
			location = self._doc.parent.parent.path
			self._doc.parent.update(set__handler=None)
		else:
			location = self._doc.parent.path
		
		try:
			self._doc.delete()
		except:
			log.exception("Error deleting an asset.")
			return dict(ok=False, message="Encountered error attempting to delete asset.")
		
		return dict(ok=True, location=location)
	
	# TODO: Decorate as embedded handler.
	def __embed__(self):
		# TODO: Extract this into a real template.
		return Markup("""<p class="error">Attempted to embed non-embeddable asset "{title}" (at {path}).</p>""".format(
				title = escape(str(self._doc)),
				path = escape(self._doc.path),
			))
