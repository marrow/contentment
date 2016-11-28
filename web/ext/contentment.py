# encoding: utf-8

import os
from functools import partial
from itsdangerous import TimestampSigner
from marrow.package.loader import load
from marrow.package.host import PluginManager
from mongoengine import ImageGridFsProxy
from urllib.parse import quote_plus, unquote_plus
from web.contentment.util import D_
from web.component.asset.model import Asset
from webob.cookies import Base64Serializer, CookieProfile


log = __import__('logging').getLogger(__name__)


def indent(context, lines, padding='\t'):
	return padding + ('\n' + padding).join(lines.split('\n'))


MAP = {
		'localhost': ('localhost', 'en', 'http://localhost:8080/'),
	}


class PlainSerializer(object):
	def dumps(self, string):
		return quote_plus(string).encode('ascii')
	def loads(self, string):
		return unquote_plus(string.decode('ascii'))


user_cookie = CookieProfile('uid', httponly=True, serializer=Base64Serializer(serializer=PlainSerializer()))


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
		
		if 'SECRET' in os.environ and 'uid' in context.request.cookies:
			s = TimestampSigner(os.environ['SECRET'])
			try:
				uc = user_cookie.bind(context.request)
				token = uc.get_value()
				token = s.unsign(token, max_age=60*60*24).decode('ascii')
			except:
				context.uid = None
				if __debug__: raise
			else:
				context.uid = token.partition('-')[2]
		else:
			context.uid = None
		
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
