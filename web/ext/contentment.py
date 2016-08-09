# encoding: utf-8

from collections import namedtuple
from functools import partial
from socket import gethostname
from marrow.package.loader import load
from marrow.package.host import PluginManager
from mongoengine import ImageGridFsProxy
from web.contentment.util import D_

from web.component.asset.model import Asset


log = __import__('logging').getLogger(__name__)


def indent(context, lines, padding='\t'):
	return padding + ('\n' + padding).join(lines.split('\n'))


DomainMapping = namedtuple('DomainMapping', ('domain', 'language', 'homepage'))

MAPPING = {'localhost': DomainMapping('localhost', None, 'http://localhost:8080/')}
try:
	_name = gethostname()
	MAPPING[_name] = DomainMapping(_name, None, None)


class ContentmentExtension:
	"""WebCore extension for managing Contentment concerns.
	
	On startup this registers and enumerates the various Contentment plugin namespaces. It provides a minimal number
	of configuration options:
	
	* `prefixed` - Use the server_name as a path prefix when looking up assets matching the current URI?
	"""
	
	needs = {'mongodb'}
	
	def __init__(self, prefixed=False):
		self.prefixed = prefixed
	
	def start(self, context):
		log.info("Starting Contentment extension.")
		
		for asset_type in PluginManager('web.component'):
			log.info("Found asset type: " + repr(asset_type))
		
		context.view.register(dict, self.render_json_response)
	
	def prepare(self, context):
		dom = context.request.host.partition(':')[0]
		parts = MAP.get(dom, (dom, 'en', ''))
		context.domain = parts[0]
		context.lang = parts[1]
		context.otherlang = parts[2]
		context.site = context.croot = Asset.objects.nearest('/' + context.domain)
		context.D = partial(D_, lang=parts[1])
		context.replacements = dict(context=context)
		
		if context.croot:
			context.theme = load(context.croot.properties.theme + ':page')
		else:
			context.theme = load('web.theme.bootstrap.base:page')
		
		log.info("Prepared context.", extra=dict(domain=[dom, context.domain], lang=context.lang, root=repr(context.croot), theme=repr(context.theme)))
	
	def render_json_response(self, context, result):
		import json
		
		response = context.response
		
		response.content_type = 'application/json'
		response.encoding = 'utf-8'
		response.text = json.dumps(result)

		return True

