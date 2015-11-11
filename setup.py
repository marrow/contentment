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


if sys.version_info < (2, 7):
	raise SystemExit("Python 2.7 or later is required.")
elif sys.version_info > (3, 0) and sys.version_info < (3, 3):
	raise SystemExit("Python 3.3 or later is required.")

exec(open(os.path.join("web", "contentment", "release.py")).read())


class PyTest(TestCommand):
	def finalize_options(self):
		TestCommand.finalize_options(self)
		
		self.test_args = []
		self.test_suite = True
	
	def run_tests(self):
		import pytest
		sys.exit(pytest.main(self.test_args))


here = os.path.abspath(os.path.dirname(__file__))

tests_require = [
		'pytest',  # test collector and extensible runner
		'pytest-cov',  # coverage reporting
		'pytest-flakes',  # syntax validation
		'pytest-cagoule',  # intelligent test execution
		'pytest-spec<=0.2.22',  # output formatting
	]


setup(
	name = "Contentment",
	version = version,
	
	description = description,
	long_description = codecs.open(os.path.join(here, 'README.rst'), 'r', 'utf8').read(),
	url = url,
	download_url = 'https://warehouse.python.org/project/Contentment/',
	
	author = author.name,
	author_email = author.email,
	
	license = 'MIT',
	keywords = '',
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
	
	packages = find_packages(exclude=['test', 'script', 'example']),
	include_package_data = True,
	namespace_packages = [
			'web',
			'web.ext',
			'web.component',
		],
	
	entry_points = {
			'web.extension': [
					'contentment = web.ext.contentment:ContentmentExtension',
					#' = web.ext.:Extension',
				],
			
			'web.component': [
					'core.asset = web.component.asset:AssetComponent',
					#' = web.component:Component',
				],
			
			'web.dispatch': [
					'contentment = web.contentment.dispatch:ContentmentDispatch',
				]
		},
	
	install_requires = [
			# 'WebCore',  # web framework  # pending 2.0 release; use requirements.txt for now
			'mongoengine',  # database layer
			'pytz',  # timzone support
			'blinker',  # signals
			'markupsafe',  # injection protection
			'babel',  # internationalization and localization
			'webassets',  # static asset management
			'tablib',  # data interchange
		],
	
	extras_require = dict(
			development = tests_require,
		),
	
	tests_require = tests_require,
	
	zip_safe = True,
	cmdclass = dict(
			test = PyTest,
		)
)
