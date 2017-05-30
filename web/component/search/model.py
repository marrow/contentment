from marrow.mongo.document import Asset
from marrow.mongo.field import Array, String, Path


class Search(Asset):
	query = String(default=None)
	base = Path(default='/')
	exclude = Array(String(), assign=True)
