# encoding: utf-8

from mongoengine import StringField

from .base import Block
from .video_ import render_video_block


class VideoBlock(Block):
	__icon__ = 'youtube-play'
	
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
	
	video = StringField(read=True, write=True)
	
	# Data Portability
	
	def __json__(self):
		return dict(super(VideoBlock, self).as_json,
				video = self.video,
			)
	
	def __html_stream__(self, context=None):
		return render_video_block(context, self)
	
	def __text__(self):
		return self.target.__text__()
