#!/usr/bin/env python3
# encoding: utf-8

import sys
from os.path import dirname, join

import cinje

from web.core.application import Application

from web.app.static import static

from web.ext.template import TemplateExtension
from web.ext.cast import CastExtension
from web.ext.local import ThreadLocalExtension
from web.ext.mongodb.mongoengine import MongoEngineExtension
from web.ext.contentment import ContentmentExtension

from web.contentment.controller import ContentmentRoot

import web.component.asset.model
import web.component.page.model


class Root(ContentmentRoot):
	static = static(join(dirname(__file__), 'static'))


app = Application(
		Root,
		logging = {
				'version': 1,
				'handlers': {
						'console': {
								'class': 'logging.StreamHandler',
								'formatter': 'json',
								# 'level': 'debug',
								'stream': 'ext://sys.stdout',
							}
					},
				'loggers': {
						'web': {
								'level': 'DEBUG',
								'handlers': ['console'],
								'propagate': False
							},
					},
				'root': {
						'level': 'INFO',
						'handlers': ['console']
					},
				'formatters': {
						'json': {
								'()': 'web.contentment.util.JSONFormatter',
								'format': '%(asctime)s\t%(levelname)s\t%(name)s:%(funcName)s:%(lineno)s  %(message)s',
								# 'force_keys': ('levelname', 'lineno'),
								
							}
					},
				
				
			},
		extensions = [
				TemplateExtension(),
				CastExtension(),
				MongoEngineExtension(uri="mongodb://localhost/contentment"),
				ContentmentExtension(),
				ThreadLocalExtension()
			]
	)


if len(sys.argv) > 1 and sys.argv[1] == 'serve':
	app.serve('waitress', host='0.0.0.0', port=8080, threads=15)
