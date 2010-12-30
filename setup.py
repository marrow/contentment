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
        
        install_requires = ['WebCore', 'beaker', 'mako', 'pymongo', 'mongoengine', 'marrow.util', 'textile', 'slate', 'pytz', 'pdfminer'],
        
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
        
        namespace_packages = ['web', 'web.extras', 'web.extras.contentment', 'web.extras.contentment.components', 'web.extras.contentment.themes', 'alacarte', 'alacarte.template'],
        
        paster_plugins = ['PasteScript', 'WebCore'],
        
        entry_points = {
                'contentment.component': [
                        "alias = web.extras.contentment.components.alias:AliasComponent",
                        "asset = web.extras.contentment.components.asset:AssetComponent",
                        "authenticator = web.extras.contentment.components.authenticator:AuthenticatorComponent",
                        "comment = web.extras.contentment.components.comment:CommentComponent",
                        "event = web.extras.contentment.components.event:EventComponent",
                        "file = web.extras.contentment.components.file:FileComponent",
                        "folder = web.extras.contentment.components.folder:FolderComponent",
                        "identity = web.extras.contentment.components.identity:IdentityComponent",
                        "page = web.extras.contentment.components.page:PageComponent",
                        "search = web.extras.contentment.components.search:SearchComponent",
                        "settings = web.extras.contentment.components.settings:SettingsComponent",
                        "theme = web.extras.contentment.components.theme:ThemeComponent",
                        
                        "default_theme = web.extras.contentment.themes.default:DefaultTheme",
                    ],
                'contentment.renderer': [
                        "raw = web.extras.contentment.components.page.renderers.raw:RawRenderer",
                        "html = web.extras.contentment.components.page.renderers.html:HTMLRenderer",
                        "textile = web.extras.contentment.components.page.renderers.textile_:TextileRenderer"
                    ],
                'contentment.file.format': [
                        "audio = web.extras.contentment.components.file.formats.audio:AudioFileFormat",
                        "image = web.extras.contentment.components.file.formats.image:ImageFileFormat",
                        "pdf = web.extras.contentment.components.file.formats.pdf:PDFFileFormat",
                        "video = web.extras.contentment.components.file.formats.video:VideoFileFormat",
                        "html = web.extras.contentment.components.file.formats.html:HTMLFileFormat",
                    ]
            },
        
    )
