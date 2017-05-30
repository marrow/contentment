# encoding: utf-8

from mongoengine import StringField, ReferenceField, PointField, IntField

from marrow.package.loader import load

from .base import Block
from .map_ import render_map_block


class MapBlock(Block):
	__icon__ = 'map'
	
	# Data Definition
	
	KINDS = [
			"place",
			"directions",
			"search",
			"view",
			"streetview",
		]
	
	STYLES = [
			"roadmap",
			"satellite",
		]
	
	kind = StringField(required=True, default='place', choices=KINDS)
	style = StringField(required=True, default='roadmap', choices=STYLES)
	
	query = StringField()
	origin = StringField()
	destination = StringField()
	avoid = StringField(default=None)  # tolls|ferries|highways
	
	center = PointField(default=None, auto_index=False)
	zoom = IntField(default=None, min_value=0, max_value=21)
	
	# Python Methods
	
	def __repr__(self, extra=None):
		return super(MapBlock, self).__repr__("{0.kind}".format(self, ', ' if extra else '', extra))
	
	# Data Portability
	
	def __json__(self):
		return dict(super(MapBlock, self).as_json,
				kind = self.kind,
				style = self.style,
				query = self.query,
				origin = self.origin,
				destination = self.destination,
				avoid = self.avoid,
				center = self.center,
				zoom = self.zoom,
			)
	
	def __html_stream__(self, context=None):
		return render_map_block(context, self)
	
	def __text__(self):
		return self.target.__text__()
