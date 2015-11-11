# encoding: utf-8

from inspect import isroutine

from webob.exc import HTTPNotFound
from marrow.package.loader import load

from web.dispatch.object import ObjectDispatch

from web.component.asset.model import Asset


log = __import__('logging').getLogger(__name__)


class ContentmentDispatch:
	def __init__(self, config):
		self._object_dispatch_chain = ObjectDispatch(config)
	
	def __call__(self, context, root):
		request = context.request
		pop = request.path_info_pop
		
		domain = 'careers.illicohodes.com'  # Hard-coded during testing.  Use: request.server_name
		search = '/' + domain + context.request.path_info.rstrip('/')  # + request.script_name ?
		
		if __debug__:
			log.debug("Starting Contentment dispatch.", extra=dict(
					request = id(request),
					script_name = request.script_name,
					path_info = request.path_info,
					root = repr(root),
					domain = domain,
					search = search,
				))
		
		# This is database-driven dispatch, so we optimize to find the deepest possible element first.
		nearest = Asset.objects.nearest(search)
		
		if not nearest:
			# No Asset could be found matching any depth of that path?  Switch to object dispatch on the root.
			yield from self._object_dispatch_chain(context, root)
			return
		
		# By stopping before we yield a "final" (retval[2] == True) value we force dispatch to re-evaluate
		# the dispatcher for the call.
		#import pudb; pu.db
		document, controller = nearest.controller
		
		yield nearest.path.split('/')[2:], controller(context, document), False
