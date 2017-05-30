from marrow.mongo.document import Asset
from marrow.mongo.field import Boolean
from marrow.mongo.trait import Redirecting


class Alias(Redirecting, Asset):
	redirect = Boolean(default=True)  # Perform an external (visible) redirection.
