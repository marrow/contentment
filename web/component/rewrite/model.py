from marrow.mongo.document import Asset, Document
from marrow.mongo.field import Array, Boolean, Embed, Regex
from marrow.mongo.trait import Linked


class Rewrite(Linked, Asset):
	class Match(Document):
		__pk__ = 'pattern'
		
		pattern = Regex()
		replacement = Regex()
		done = Boolean(default=False)
	
	match = Array(Embed('.Match'), assign=True)
