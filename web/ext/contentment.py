# encoding: utf-8

from web.core import local
from web.core.response import registry
from marrow.package.loader import load
from marrow.package.host import PluginManager
from mongoengine import ImageGridFsProxy

from web.component.asset.model import Asset


log = __import__('logging').getLogger(__name__)


def indent(context, lines, padding='\t'):
	return padding + ('\n' + padding).join(lines.split('\n'))


MAP = {
		'localhost': ('career.nse-automatech.com', 'fr', 'http://localhost:8080/'),
		
		# NSE Automatech
		# Testing URLs
		'en.nse.illico.cleverapps.io': ('career.nse-automatech.com', 'en', 'fr.nse.illico.cleverapps.io'),
		'fr.nse.illico.cleverapps.io': ('career.nse-automatech.com', 'fr', 'en.nse.illico.cleverapps.io'),
		# Production URLs
		'career.nse-automatech.com': ('career.nse-automatech.com', 'en', 'http://carrieres.nse-automatech.com'),
		'carrieres.nse-automatech.com': ('career.nse-automatech.com', 'fr', 'http://career.nse-automatech.com'),
		
	}


class ContentmentExtension:
	needs = ('template', )
	
	def __call__(self, context, app):
		def protected_inner(environ, start_response=None):
			try:
				return app(environ, start_response)
			except:
				if __debug__:
					try:
						import pudb; pudb.post_mortem()
					except:
						pass
				raise
		
		return protected_inner
	
	def start(self, context):
		log = __import__('logging').getLogger(__name__)
		log.info("Starting Contentment extension.")
		context.namespace.indent = indent
		
		for asset_type in PluginManager('web.component'):
			log.info("Found asset type: " + repr(asset_type))
		
		registry.register(self.render_gridfs_image, ImageGridFsProxy)
	
	def prepare(self, context):
		dom = context.request.host.partition(':')[0]
		parts = MAP.get(dom, (dom, 'en'))
		context.domain = parts[0]
		context.lang = parts[1]
		context.otherlang = parts[2]
		context.croot = Asset.objects.nearest('/' + context.domain)
		
		if context.croot:
			context.theme = load(context.croot.properties.theme + ':page')
		else:
			context.theme = load('web.theme.bootstrap.base:page')
		
		local.context = context
		
		log.info("Prepared context.", extra=dict(domain=[dom, context.domain], lang=context.lang, root=repr(context.croot), theme=repr(context.theme)))
	
	def render_gridfs_image(self, context, result):
		response = context.response
		
		response.content_type = 'image/' + result.format.lower()
		result.seek(0)
		response.body = result.read()
		
		return True
