# encoding: utf-8

from marrow.package.canonical import name as name_
from marrow.schema import Attribute
from marrow.mongo.query import Ops

if __debug__:
	import time


log = __import__('logging').getLogger(__name__)


class Taxonomy(Ops):
	"""A factory for marrow.mongo queries relating to taxonomic structure."""
	
	collection = Attribute()
	
	# Query Terminals
	# These prevent further chaining by immediately executing the query to return a result.
	
	def scalar(self, *fields):
		"""Retrieve the given field or fields from the filtered assets.
		
		If only a single field is given, an iterable of just that field is returned. If multiple fields are being
		selected, you'll get back an iterable of tuples of those fields in the same order.
		"""
		
		if __debug__:  # Give useful error messages in development.
			if 'collection' not in self.__data__ or not self.collection:
				raise RuntimeError("Called method requiring bound collection without one.")
		
		projection = {'_id': 0}  # Exclude the ID by default.
		projection.update({field: 1 for field in fields})  # Add explicit inclusion for named fields.
		
		results = self.collection.find(self.as_query, projection)
		
		if len(fields) == 1:  # Special case for single field scalars.
			field = fields[0]
			
			for result in results:
				yield result.get(field)
			
			return
		
		# Slightly simpler multi-field scalars.
		for result in results:
			yield tuple(result.get(field, None) for field in fields)
	
	def nearest(self, path, projection=None):
		"""Immediately look up the asset nearest the given path, utilizing any query built so far.
		
		Allows for optional projection. This must immediately issue the query due to the fairly complex query.
		"""
		
		if __debug__:  # Give useful error messages in development.
			if 'collection' not in self.__data__ or not self.collection:
				raise RuntimeError("Called method requiring bound collection without one.")
		
		if hasattr(path, 'split'):  # We accept iterables of individual elements, or a string.
			path = path.split('/')
		else:
			path = list(path)
		
		# Remove leading empty elements.
		while path and not path[0]:
			del path[0]
		
		# Remove trailing empty elements.
		while path and not path[-1]:
			del path[-1]
		
		# Determine the full list of possible paths and prepare the query.
		paths = [('/' + '/'.join(path[:i])) for i in range(len(path) + 1)]
		criteria = (self & {'path': {'$in': paths}}).as_query
		
		if hasattr(projection, 'as_projection'):
			projection = projection.as_projection
		
		if __debug__:
			log.debug("Searching for asset nearest: /" + '/'.join(path), extra=dict(
					query = criteria,
					projection = projection
				))
		
		# Issue the query against our bound collection.
		result = self.collection.find_one(criteria, projection, sort=(('path', -1), ))
		
		return result
	
	# Basic Queries
	# These cover fairly basic attributes of asset documents, for convienence.
	
	def named(self, name):
		"""Filter to assets with a given name, useful primarily when chained with other criteria."""
		return self & {'name': name}
	
	def of_type(self, kind):
		"""Restrict to instances of specific Asset subclasses.
		
		Unlike an `isinstance()` check, this is explicit and does not include subclasses of the target class.
		"""
		if not isinstance(kind, str):
			kind = name_(kind)
		
		return self & {'_cls': kind}
	
	# Asset Management
	# Basic management operations.
	
	def empty(self):
		"""Delete all descendants of the currently filtered assets.
		
		Because this is removing every single descendant, there is no need to update asset ordering. Allows chaining
		as the parent elements (currently filtered elements) remain.
		
		Because this is an operation against the descendants, not containers, no modification times are updated.
		"""
		
		if __debug__:  # Give useful error messages in development.
			if 'collection' not in self.__data__ or not self.collection:
				raise RuntimeError("Called method requiring bound collection without one.")
		
		result = self.collection.delete_many(self.descendants.as_query)
		
		log.warn("Deleted %d assets.", result.deleted_count)
		
		return self
	
	def detach(self):
		"""Detach the target assets from the taxonomy.
		
		Detached assets have technically invalid paths; ones not starting with `/`. This makes them easy to detect
		while also preserving the association with their descendants. Allows chaining, albiet by returning a new
		Taxonomy query filtering for the detached assets by `_id`. Due to needing to update several values on each
		affected document, including one which is calculated, a query is placed, then a bulk update operation
		prepared and executed. This won't be the fastest operation in the world if detaching too many assets at once.
		
		This operation updates the modification time of the affected assets and allows chaining by returning a new
		Taxononmy query selecting the target elements by `_id`.
		"""
		
		if __debug__:  # Give useful error messages in development.
			count = 0
			if 'collection' not in self.__data__ or not self.collection:
				raise RuntimeError("Called method requiring bound collection without one.")
		
		extra = {k: v for k, v in self.__data__.items() if k != 'operations'}
		targets = list(self.scalar('_id', 'parents', 'name'))
		updates = self.collection.initialize_unordered_bulk_op()
		
		if __debug__:
			start = time.time()  # Operation building duration.
			log.debug("Preparing updates for asset detachment.")
		
		for target, target_parents, name in targets:
			updates.find({'_id': target}).update_one({'$currentDate': {'updated': 'date'}, '$set': {
					'path': name,
					'parent': None,
					'parents': []
				}})
			
			if __debug__:
				count += 1
				log.debug("Updating target asset.", extra(updated="<now>", path=name, parent=None, parents=[]))
			
			for descendant, parents, name in self.__class__({}, **extra).scalar('_id', 'parents', 'name'):
				# Because we embed some of the properties of the parents in the array we are careful in how we prune.
				
				del parents[:len(target_parents)]  # This approach preserves all attributes, without introspection.
				path = '/'.join(parent['name'] for parent in parents) + '/' + name  # String concatenation is fast.
				
				updates.find({'_id': descendant}).update_one({'$currentDate': {'updated': 'date'},
						'$set': {'path': path, 'parents': parents}})
				
				if __debug__:
					count += 1
					log.debug("Updating desendant asset.", extra(updated="<now>", path=path, parents=parents))
		
		if __debug__:
			log.debug("Preparation complete.", extra=dict(duration=time.time() - start))
			start = time.time()
			log.debug("Executing %d bulk update%s.", count, "" if count == 1 else "s", extra=dict(count=count))
		
		result = updates.execute()
		
		if __debug__:
			log.debug("Bulk update%s complete.", "" if count == 1 else "s",
					extra=dict(count=count, duration=time.time() - start, result=result))
		
		ntargets = len(targets)
		if result.nModified == ntargets:
			log.info("Detached %d asset%s.", ntargets, "" if ntargets == 1 else "s")
		else:
			dupdates = result.nModified - ntargets
			log.info("Detached %d asset%s and %d descendant%s.", ntargets, "" if ntargets == 1 else "s",
					dupdates, "" if dupdates == 1 else "s")
		
		return self.__class__({'_id': {'$in': [target[0] for target in targets]}}, **extra)
	
	# Taxonomy Querying
	# These are properties where possible to make chaining more elegant.
	
	@property
	def children(self):
		"""A Taxonomy query selecting for the immediate children of the filtered assets."""
		extra = {k: v for k, v in self.__data__.items() if k != 'operations'}
		return self.__class__({'parent': {'$in': self.scalar('_id')}}, **extra)
	
	@property
	def descendants(self):
		"""A Taxonomy query selecting for all descendants of the filtered assets."""
		extra = {k: v for k, v in self.__data__.items() if k != 'operations'}
		return self.__class__({'parents._id': {'$in': self.scalar('_id')}}, **extra)
		
		# Alternate approach... TODO: test the performance difference here.
		# path = (re.compile('^' + re.escape(path + '/')) for path in self.scalar('path'))
		# return self.__class__({'path': {'$in': paths}}, **extra)

