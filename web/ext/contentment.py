# encoding: utf-8

from marrow.package.host import PluginManager


def indent(context, lines, padding='\t'):
	return padding + ('\n' + padding).join(lines.split('\n'))


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
		
		# registry.register(render_asset, Asset)
