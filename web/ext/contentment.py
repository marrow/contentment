# encoding: utf-8

from functools import partial
from marrow.package.loader import load
from marrow.package.host import PluginManager
from mongoengine import ImageGridFsProxy
from web.contentment.util import D_

from web.component.asset.model import Asset


log = __import__('logging').getLogger(__name__)


def indent(context, lines, padding='\t'):
	return padding + ('\n' + padding).join(lines.split('\n'))


MAP = {
		'localhost': ('career.nse-automatech.com', 'fr', 'http://localhost:8080/'),
		
		# NSE Automatech
		'app-15b75793-4441-4fe2-9c12-1f13b90d00be.cleverapps.io': ('career.nse-automatech.com', 'en', 'http://app-15b75793-4441-4fe2-9c12-1f13b90d00be.cleverapps.io'),
		# Testing URLs
		'en.nse.illico.cleverapps.io': ('career.nse-automatech.com', 'en', 'fr.nse.illico.cleverapps.io'),
		'fr.nse.illico.cleverapps.io': ('career.nse-automatech.com', 'fr', 'en.nse.illico.cleverapps.io'),
		# Production URLs
		'career.nse-automatech.com': ('career.nse-automatech.com', 'en', 'http://carrieres.nse-automatech.com'),
		'carrieres.nse-automatech.com': ('career.nse-automatech.com', 'fr', 'http://career.nse-automatech.com'),
	}


class ContentmentExtension:
	needs = ()
	
	def start(self, context):
		log = __import__('logging').getLogger(__name__)
		log.info("Starting Contentment extension.")
		
		for asset_type in PluginManager('web.component'):
			log.info("Found asset type: " + repr(asset_type))
		
		context.view.register(dict, self.render_json_response)
		context.view.register(ImageGridFsProxy, self.render_gridfs_image)
	
	def prepare(self, context):
		dom = context.request.host.partition(':')[0]
		parts = MAP.get(dom, (dom, 'en'))
		context.domain = parts[0]
		context.lang = parts[1]
		context.otherlang = parts[2]
		context.croot = Asset.objects.nearest('/' + context.domain)
		context.D = partial(D_, lang=parts[1])
		
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
	
	def render_gridfs_image(self, context, result):
		response = context.response
		
		response.content_type = 'image/' + result.format.lower()
		result.seek(0)
		response.body = result.read()
		
		return True
