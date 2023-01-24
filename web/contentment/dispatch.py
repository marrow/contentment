# encoding: utf-8

from inspect import isroutine

from ..component.asset.model import Asset


log = __import__('logging').getLogger(__name__)


class ContentmentDispatch:
	__slots__ = []
	
	def __repr__(self):
		return "{self.__class__.__name__}(0x{id})".format(self=self, id=id(self))
	
	def __call__(self, context, obj, path):
		#__import__('wdb').set_trace()
		# TODO: Move into web.dispatch.meta as "FallbackDispatch".
		# First, try with object dispatch.  This handles custom root controller attachments such as statics.
		try:
			result = list(context.dispatch['object'](context, obj, path))
		except LookupError:
			pass
		else:
			if result and result[-1][2] and isroutine(result[-1][1]):  # Endpoint found.
				yield from result
				return
			
			del result
		
		if __debug__:
			log.debug("Starting Contentment dispatch.", extra=dict(
					request = id(context.request),
					script_name = context.request.script_name,
					path_info = context.request.path_info,
					obj = repr(obj),
					search = context.request.path_info,
				))
		
		# This is database-driven dispatch, so we optimize to find the deepest possible element first.
		nearest = Asset.objects.nearest(context.request.path_info)
		
		if not nearest:  # No Asset could be found, and root dispatch already failed.
			return
		
		# By stopping before we yield a "final" (retval[2] == True) value we force dispatch to re-evaluate
		# the dispatcher for the call.
		document, controller = nearest.controller
		
		context.asset = document
		
		yield nearest.path.split('/')[1:], controller(context, document), False
