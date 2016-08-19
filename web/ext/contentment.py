# encoding: utf-8

from marrow.package.loader import load
from marrow.package.host import PluginManager

from web.core.context import Context
from web.core.util import lazy


log = __import__('logging').getLogger(__name__)


class ContentmentContext(Context):
	@lazy
	def site(self):
		"""Retrieve the site root from the database.
		
		This is colocation aware, i.e. will attempt to look up the path `/<domain>`, falling back automatically to
		retrieval of the literal root Asset.  There is no particular additional overhead for this fallback behaviour.
		"""
		
		return self.taxonomy.nearest('/' + self._ctx.request.domain)
	
	@lazy
	def theme(self):
		"""Retrieve the active site theme.
		
		This must be an object API-compatible with the `page` template from `cinje.std.html`.
		"""
		
		theme = self.site.properties.get('theme', 'cinje.std.html:page')
		
		if ':' not in theme:
			theme += ':page'
		
		return load(theme)
	
	@lazy
	def replacements(self):
		"""A dictionary used to perform simple template-like variable replacement in generated chunks."""
		return {'context': self._ctx}


class ContentmentExtension:
	"""WebCore extension for managing Contentment concerns."""
	
	needs = {'mongodb', 'serialization'}
	provides = {'contentment'}
	extensions = {'web.component'}
	
	def start(self, context):
		"""Service startup support code to register and enumerate plugin namespaces."""
		
		for namespace in self.extensions:
			if __debug__:
				log.debug("Preparing Contentment plugin namespace: " + namespace)
			
			setattr(self, namespace.rpartition('.')[2], PluginManager(namespace))
		
		if __debug__:
			log.debug("Contentment has finished starting.")
	
	def prepare(self, context):
		"""Prepare the request-local execution context by adding our own context to it."""
		context.contentment = ContentmentContext(_ctx=context)  # Instantiate the ContentmentContext for this request.
		
		if __debug__:
			log.debug("Contentment context prepared.")

