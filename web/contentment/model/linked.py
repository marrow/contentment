from marrow.mongo import Document


class Linked(Document):
	link = Reference('Asset')
