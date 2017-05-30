from marrow.mongo.document import Asset, Document
from marrow.mongo.field import Binary, Embed, String, PluginReference


class Upload(Asset):
	"""An uploaded binary file."""
	
	class Cache(Document):
		"""The core details of an uploaded file of 1MiB or less, stored within the Asset record."""
		
		name = String(default=None)
		mime = String(defualt='application/octet-stream')
		data = Binary()
	
	handler = Asset.handler.adapt(default='upload.default')
	backend = PluginReference('web.storage', default='gridfs')
	cache = Embed('.Cache', default=None)
