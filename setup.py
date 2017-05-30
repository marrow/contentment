#!/usr/bin/env python

import os
import sys
import codecs

from setuptools import setup, find_packages


if sys.version_info < (3, 4):
	raise SystemExit("Python 3.4 or later is required.")

version = description = url = author = ''  # Actually loaded on the next line; be quiet, linter.
exec(open(os.path.join("web", "contentment", "release.py")).read())


here = os.path.abspath(os.path.dirname(__file__))


tests_require = [
		'pytest>=3.1',  # test collector and extensible runner
		
		'pytest-catchlog',  # log capture
		'pytest-cov',  # coverage reporting
		'pytest-flakes',  # syntax validation
		'pytest-isort',  # import ordering
		'pytest-pudb',  # interactive debugging
	]


setup(
	name = "Contentment",
	version = version,
	description = description,
	long_description = codecs.open(os.path.join(here, 'README.rst'), 'r', 'utf8').read(),
	url = url,
	author = author.name,
	author_email = author.email,
	license = 'MIT',
	keywords = ['mongodb', 'cms', 'content management', 'component management', 'cmf', 'marrow'],
	classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Environment :: Console",
			"Environment :: Web Environment",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python",
			"Programming Language :: Python :: 3.4",
			"Programming Language :: Python :: Implementation :: CPython",
			"Programming Language :: Python :: Implementation :: PyPy",
			"Topic :: Internet :: WWW/HTTP :: WSGI",
			"Topic :: Software Development :: Libraries :: Python Modules",
		],
	
	packages = find_packages(exclude=['test', 'example', 'benchmark', 'htmlcov']),
	include_package_data = True,
	package_data = {'': ['README.rst', 'LICENSE.txt']},
	namespace_packages = ['web', 'web.component', 'web.dispatch', 'web.ext'],
	zip_safe = False,
	
	# Dependencies
	
	setup_requires = ['pytest-runner'] if {'pytest', 'test', 'ptr'}.intersection(sys.argv) else [],
	
	install_requires = [
			'WebCore>=2.0.3,<3',  # web framework
			
			'cinje<2',  # template engine
			'markupsafe>=1,<2',  # injection protection, advanced formatting, self-rendering protocol
			'marrow.mongo[logger,markdown]>=1.1.1,<2.0',  # MongoDB-backed declarative schema, tools
			'marrow.package<2.0',  # dynamic execution and plugin management
			'web.db>=2.0.1,<3',  # database adapter layer
			'web.dispatch.resource',  # verb-based restful API interfaces
		],
	
	extras_require = dict(
			development = tests_require + [
					'pre-commit',
					'WebCore[development]>=2.0.3,<3',
				],
			markdown = ['marrow.mongo[markdown]>=1.1.1,<2.0'],
		),
	
	tests_require = tests_require,
	
	# Plugin Registration
	
	entry_points = {
			'marrow.mongo.document': [  # document class registry for name-based loading
					'Asset = web.component.asset.model:Asset',
					'Page = web.component.page.model:Page',
					'Site = web.component.site.model:Site',
					'Theme = web.component.theme.model:Theme',
					'Upload = web.component.upload.model:Upload',
					#' = web.component..model:',
					# Note: Import the class here from its real, original location to benefit from shortening.
				],
			
			'web.block': [  # self-rendering blocks
					'core.button = web.block:Block',
					'core.description = web.block:Block',
					'core.image = web.block:Block',
					'core.map = web.block:Block',
					'core.quote = web.block:Block',
					'core.reference = web.block:Block',
					'core.text = web.block:Block',
					'core.video = web.block:Block',
					#' = web.block:Block',
				],
			
			'web.component': [  # high-level resource and collection components
					'core.asset = web.component.asset:AssetComponent',
					'core.page = web.component.page:PageComponent',
					'core.site = web.component.site:SiteComponent',
					'core.theme = web.component.theme:ThemeComponent',
					'core.upload = web.component.upload:UploadComponent',
					#' = web.component:Component',
				],
			
			'web.content': [
					'core.basic = web.content.sanitize:BasicContent',
					'core.bbcode = web.content.bbcode:BBCodeContent',
					'core.markdown = web.content.markdown:MarkdownContent',
					'core.sanitize = web.content.sanitize:SanitizedContent',
					'core.template = web.content.template:TemplateContent',
					#' = web.content:Content',
				],
			
			'web.dispatch': [  # WebCore custom dispatcher
					'contentment = web.dispatch.contentment:ContentmentDispatch',
					#' = web.dispatch:Dispatch',
				],
			
			'web.extension': [  # WebCore framework extensions
					'contentment = web.ext.contentment:ContentmentExtension',
					#' = web.ext.:Extension',
				],
			
		},
)
