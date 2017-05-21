log = __import__('logging').getLogger(__name__)


class AssetController:
	__dispatch__ = 'resource'
	
	def __init__(self, context, document):
		self._ctx = context
		self._doc = document
		
		log.info("Loaded asset.", extra=dict(asset=repr(document.id)))
