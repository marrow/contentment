#!/usr/bin/env python
# encoding: utf-8

import sys, os

try:
    from distribute_setup import use_setuptools
    use_setuptools()

except ImportError:
    pass

from setuptools import setup, find_packages


if sys.version_info <= (2, 5):
    raise SystemExit("Python 2.5 or later is required.")

if sys.version_info >= (3,0):
    def execfile(filename, globals_=None, locals_=None):
        if globals_ is None:
            globals_ = globals()
        
        if locals_ is None:
            locals_ = globals_
        
        exec(compile(open(filename).read(), filename, 'exec'), globals_, locals_)

else:
    from __builtin__ import execfile

execfile(os.path.join("web", "extras", "contentment", "release.py"), globals(), locals())



setup(
        name = name,
        version = version,
        
        description = summary,
        long_description = description,
        author = author,
        author_email = email,
        url = url,
        download_url = download_url,
        license = license,
        keywords = '',
        
        install_requires = ['WebCore', 'Mako', 'pymongo<1.9', 'mongoengine', 'marrow.util', 'textile'],
        
        test_suite = 'nose.collector',
        tests_require = ['nose', 'coverage', 'nose-achievements'],
        
        classifiers = [
                "Development Status :: 2 - Beta",
                "Environment :: Console",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Programming Language :: Python",
                "Programming Language :: Python :: 3",
                "Topic :: Software Development :: Libraries :: Python Modules"
            ],
        
        packages = find_packages(exclude=['tests', 'tests.*', 'docs']),
        include_package_data = True,
        package_data = {
                '': ['Makefile', 'README.textile', 'LICENSE', 'distribute_setup.py'],
                'docs': ['source/*']
            },
        zip_safe = False,
        
        namespace_packages = ['web', 'web.extras', 'web.extras.contentment', 'web.extras.contentment.components'],
        
        paster_plugins = ['PasteScript', 'WebCore'],
        
        entry_points = {
                'contentment.component': [
                        "asset = web.extras.contentment.components.asset:AssetComponent",
                        "folder = web.extras.contentment.components.folder:FolderComponent",
                        "identity = web.extras.contentment.components.identity:IdentityComponent",
                        "page = web.extras.contentment.components.page:PageComponent",
                        "default_theme = web.extras.contentment.themes.default:DefaultTheme",
                        # "file = web.extras.contentment.components.file:FileComponent",
                        # "extension = web.extras.contentment.components.extension:ExtensionComponent"
                    ],
                'contentment.renderer': [
                        # "raw = web.extras.contentment.components.page.renderers.raw:RawRenderer",
                        # "html = web.extras.contentment.components.page.renderers.html:HTMLRenderer",
                        # "genshi = web.extras.contentment.components.page.renderers.templated:GenshiRenderer",
                        # "rest = web.extras.contentment.components.page.renderers.rest:RestRenderer"
                    ]
            },
        
    )
