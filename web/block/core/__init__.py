# encoding: utf-8

import re

from markupsafe import Markup

from marrow.mongo import Document, Index
from marrow.mongo.trait import Derived, Queryable




INITIAL_CAPS = re.compile('(.)([A-Z][a-z]+)')
CAMEL_CASE = re.compile('([a-z0-9])([A-Z])')




class Block(Derived, Queryable):
	__database__ = 'default'
	__collection__ = 'block'
	
	class Placement(Document):
		location = Reference()
		position = Integer(default=0)
	
	language = String(default=None)
	places = Array(Embed('.Placement'), assign=True)
	
	acl = Array(Embed(), assign=True)
	tag = Set(String(), assign=True)
	attr = Array(Embed(Property), assign=True)
	
	_place = Index('places.page', 'places.position', unique=True)  # Two objects may not occupy the same space.
	
	# Legacy Fields
	
	properties = Embed(Document, assign=True)
	
	# Query Methods
	
	@classmethod
	def blocks_for(cls, page, language=None):
		q = cls.places.page == page
		
		if language:
			q &= cls.language == language
		
		for record in cls.find(q, sort=('places__S__position', )):
			yield cls.from_mongo(record)
	
	def insert_block(self, content, index=None, create=True):
		"""Add a block to the page, either at the end of the available blocks, or at a specific index."""
		# TODO: Allow for insertion of multiple blocks using iterable ABC.
		
		content = content.to_mongo() if hasattr(content, 'to_mongo') else content
		
		if create:
			content['id'] = ObjectId()  # Ensure we always have a unique ID.
		
		update = {
				'$push': {
						'content': {'$each': [content]}
					}
			}
		
		if index is not None:
			update['$push']['content']['$position'] = index
		
		return self.update(__raw__=update)
	
	def update_block(self, id=None, index=None, raw=None, **kw):
		"""Update a block on a page by ID or index using MongoEngine-alike semantics.
		
		Passing a `raw` value will merge it with the overall Page query, not the block-speicifc one, allowing for
		additional conditional criteria about the surrounding page.
		"""
		if id is None and index is None:
			raise ValueError()
		
		if id is not None and index is not None:
			raise ValueError()
		
		ops = ('set', 'unset', 'inc', 'dec', 'push', 'push_all', 'pop', 'pull', 'pull_all', 'add_to_set')
		update = dict()
		
		for key, value in kw.items():
			parts = key.split('__')
			parts.insert(1 if parts[0] in ops else 0, 'content__$' if id else 'content__' + str(index))
			update['__'.join(parts)] = value
		
		if raw:
			update.update(raw)
		
		return self.__class__.objects(id=self.id, content__id=id).update(**update)
	
	def remove_block(self, id=None, index=None):
		"""Remove a block by id or index."""
		if id is None and index is None:
			raise ValueError()
		
		if id is not None and index is not None:
			raise ValueError()
		
		if index:
			id = self.content[index].id
		
		return self._collection.update_one({'_id': self.id}, {'$pull': {'content': {'id': id}}})
	
	def move_block(self, id, index):
		"""Move a block to a new index.
		
		NOTE: The new index is post-removal, i.e. it does not adjust if the insertion point is after the original index.
		"""
		
		# TODO: Apply this in a single operation.
		coll = self.__class__._get_collection()
		block = coll.find_one({'_id': self.id, 'content.id': id}, {'content.$': 1})['content'][0]
		self.remove_block(id)
		self.insert_block(block, index, create=False)
	
	
	
	# Visualization
	
	@property
	def name(self):
		"""An unencoded version of the class name.
		
		Converts various forms of camel-case (i.e. `AwesomeThingBlock`) into space-separated segments, with any instances
		of `Block` removed.  (I.e. `Awesome Thing`)
		"""
		name = self.__class__.__name__.replace('Block', '')
		name = INITIAL_CAPS.sub(r'\1 \2', name)
		return CAMEL_CASE.sub(r'\1 \2', name)
	
	def __tree__(self, indent=''):
		print(indent, repr(self), sep='')
	
	# Python Methods
	
	def __str__(self):
		return "{label}: #{self.id!s}".format(self=self, label=self.__class__.__name__.replace('Block', ''))
	
	def __repr__(self, extra=None):
		return "{0.__class__.__name__}({0.id}{1}{2}, {0.properties!r})".format(self, ', ' if extra else '', extra)
	
	# Data Portability
	
	def __json__(self):
		return {
				'id': self.id,
				'type': self.__class__.__name__
			}
	
	as_json = property(lambda self: self.__json__())
	
	def __html_stream__(self, context=None):
		return []
	
	as_stream = property(lambda self: self.__html_stream__)  # Note: doesn't call!
	
	def __html__(self):
		return "".join(self.__html_stream__())
	
	as_html = property(lambda self: self.__html__())
	
	def __text__(self):
		return ""
	
	as_text = property(lambda self: self.__text__())

	__xml__ = block

	as_xml = property(lambda self: self.__xml__())
