from marrow.mongo.field import Integer
from marrow.mongo.trait import Linked


class Redirecting(Linked):
	status = Integer(default=302, choices=[301, 302])  # If redirecting, which status code should be utilized?
	
	@property
	def redirect_exception(self):
		"""Return the appropriate WebOb representation for this exception."""
		
		pass
