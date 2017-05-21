#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import os
import sys
import codecs


try:
	from setuptools.core import setup, find_packages
except ImportError:
	from setuptools import setup, find_packages

from setuptools.command.test import test as TestCommand


if sys.version_info < (3, 4):
	raise SystemExit("Python 3.4 or later is required.")

version = description = url = author = ''  # Actually loaded on the next line; be quiet, linter.
exec(open(os.path.join("web", "contentment", "release.py")).read())


here = os.path.abspath(os.path.dirname(__file__))

py2 = sys.version_info < (3,)
py26 = sys.version_info < (2, 7)
py32 = sys.version_info > (3,) and sys.version_info < (3, 3)
pypy = hasattr(sys, 'pypy_version_info')


tests_require = [
		'pytest',  # test collector and extensible runner
		'pytest-cov',  # coverage reporting
		'pytest-flakes',  # syntax validation
		'pytest-catchlog',  # log capture
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
			'WebCore>=2.0,<3.0',  # web framework
			'marrow.mongo>=1.1.1,<2.0',  # database layer
			'cinje>=1.0,<2.0',  # template engine
		],
	
	extras_require = dict(
			development = tests_require + ['pre-commit'],
		),
	
	tests_require = tests_require,
	
	# Plugin Registration
	
	entry_points = {
			'marrow.mongo.document': [
					'Asset = web.component.asset.model:Asset',
				],
			'web.component': [
					'core.asset = web.component.asset:AssetComponent',
					#' = web.component:Component',
				],
			'web.dispatch': [
					'contentment = web.dispatch.contentment:ContentmentDispatch',
				],
			'web.extension': [
					'contentment = web.ext.contentment:ContentmentExtension',
					#' = web.ext.:Extension',
				],
		},
)
