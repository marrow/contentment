from marrow.mongo import Document
from marrow.mongo.field import Array, Embed, Set, String, PluginReference


class Style(Document):
	# Template engine stuff.
	container = PluginReference('cinje.container', default=None)  # The cinje wrapping template to use.
	attributes = Embed(Document, default=None)  # Arguments to the cinje wrapping template.
	
	# Core CSS selectors: HTML identifier and CSS classes.
	identifier = String(default=None)  # The HTML identifier.
	classes = Set(String(), assign=True)  # CSS classes applied.
	
	# Theme stuff.
	selectors = Array(Embed('Property'), assign=True)  # Custom CSS selector to theme mappings.
