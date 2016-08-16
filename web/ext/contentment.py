# encoding: utf-8

from collections import namedtuple
from socket import gethostname
from marrow.package.loader import load
from marrow.package.canonical import name
from marrow.package.host import PluginManager

from web.core.context import Context


log = __import__('logging').getLogger(__name__)


# If the language is None, it will be inferred normally.
DomainMapping = namedtuple('DomainMapping', ('domain', 'language'))

MAPPING = {'localhost': DomainMapping('localhost', None)}
try:
	_name = gethostname()
	MAPPING[_name] = DomainMapping(_name, None)
except:
	pass


class ContentmentExtension:
	"""WebCore extension for managing Contentment concerns.
	
	On startup this registers and enumerates the various Contentment plugin namespaces.
	"""
	
	needs = {'mongodb', 'serialization'}
	provides = {'contentment'}
	extensions = {'web.component'}
	
	def __init__(self):
		self.context = Context(mapping=dict(MAPPING))
	
	def start(self, context):
		log.info("Starting Contentment extension.")
		c9t = context.contentment = self.context.promote('ContentmentContext', False)
		
		for namespace in self.extensions:
			if __debug__:
				log.debug("Preparing Contentment plugin namespace: " + namespace)
			
			setattr(c9t, namespace.rpartition('.')[2], PluginManager(namespace))
	
	def prepare(self, context):
		req = context.request
		c9t = context.contentment = context.contentment()  # Instantiate the ContentmentContext for this request.
		
		c9t.domain = c9t.domain_mapping.get(req.server_name, DomainMapping(req.server_name, None))
		c9t.site = c9t.taxonomy.nearest('/' + c9t.domain)  # TODO: Defer or cache this?
		c9t.replacements = dict(context=context)
		
		# We allow for colocation of sites, so we need to pull this out of the active site on demand.  TODO: Defer?
		if c9t.site and 'theme' in c9t.site.properties:
			c9t.theme = load(c9t.site.properties.theme + ':page')
		else:
			c9t.theme = load('web.theme.bootstrap.base:page')
		
		if __debug__:
			log.debug("Prepared Contentment context.", extra=dict(domain=c9t.domain, site=repr(c9t.site), theme=name(context.theme)))

