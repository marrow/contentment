log = __import__('logging').getLogger(__name__)


class ContentmentExtension:
	"""WebCore extension for managing Contentment concerns."""
	
	needs = {'mongodb', 'serialization'}
	provides = {'contentment'}
	extensions = {'web.component'}
