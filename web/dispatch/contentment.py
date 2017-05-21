from ..component.asset import Asset


log = __import__('logging').getLogger(__name__)


class ContentmentDispatch:
	__slots__ = []
	
	def __repr__(self):
		return "{self.__class__.__name__}(0x{id})".format(self=self, id=id(self))
	
	def __call__(self, context, obj, path):
		# TODO: Fetch current-language locale content only.
		
		if __debug__:
			log.debug("Starting Contentment dispatch.", extra=dict(
					request = id(context.request),
					script_name = context.request.script_name,
					path_info = context.request.path_info,
					obj = repr(obj),
					search = context.request.path_info,
				))
		
		# Identify the site root using the current host name as a form of virtual hosting.
		
		site = context.site = Asset.get_nearest('/' + '/'.join(reversed(context.request.server_name.split('.'))))
		if not site: raise LookupError("Failed to identify site root.")
		
		depth = len(site.path)  # The number of elements to strip off asset paths when yielding.
		apath = site.path / '/'.join(path)
		asset = site
		
		yield None, site, False  # Announce discovery of site root.
		
		# This is database-driven dispatch, so we optimize to find the deepest possible element first.
		
		if __debug__:
			log.debug("Attempting to identify asset nearest path: " + str(apath))
		
		for asset in Asset.find_nearest(apath, site.descendants):
			yield asset.path.parts[depth:], asset, False
			depth = len(asset.path.parts)
		
		context.asset = asset
		
		# By stopping before we yield a "final" (retval[2] == True) value we force dispatch to re-evaluate.
		yield None, asset.handler(context, nearest), False
