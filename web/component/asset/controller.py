# encoding: utf-8

from webob.exc import HTTPNotFound
from markupsafe import Markup, escape

from .model import Asset

log = __import__('logging').getLogger(__name__)


class AssetController:
	def __init__(self, context, document):
		self._ctx = context
		self._doc = document
		
		log.info("Loaded asset.", extra=dict(asset=repr(document.id)))
	
	# TODO: Decorate as embedded handler.
	def __embed__(self):
		# TODO: Extract this into a real template.
		return Markup("""<p class="error">Attempted to embed non-embeddable asset "{title}" (at {path}).</p>""".format(
				title = escape(str(self._doc)),
				path = escape(self._doc.path),
			))
