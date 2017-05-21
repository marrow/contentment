===========
Contentment
===========

|latestversion| |ghtag| |masterstatus| |mastercover| |masterhealth| |masterreq| |ghwatch| |ghstar|

    © 2010-2017 Alice Bevan-McGregor and contributors.

..

    https://github.com/marrow/contentment

..


Contentment is a component management framework (CMF) focusing on server-side DOM construction, streaming generation,
modular design, and a rich MongoDB-based data storage engine.

Additional documentation is provided in the form of an `online reference manual <https://contentment.webcore.io/>`__.


Installation
============

Installing ``Contentment`` is easy, just execute the following in a terminal::

    pip install contentment

**Note:** We *strongly* recommend always using a container, virtualization, or sandboxing environment of some kind when
developing using Python; installing things system-wide is yucky (for a variety of reasons) nine times out of ten.  We
prefer light-weight `virtualenv <https://virtualenv.pypa.io/en/latest/virtualenv.html>`__, others prefer solutions as
robust as `Vagrant <http://www.vagrantup.com>`__.

If you add ``contentment`` to the ``install_requires`` argument of the call to ``setup()`` in your application's
``setup.py`` file, marrow.mongo will be automatically installed and made available when your own application or
library is installed.  We recommend using "less than" version numbers to ensure there are no unintentional
side-effects when updating.  Use ``contentment<3.1`` to get all bugfixes for the current release, and
``contentment<4.0`` to get bugfixes and feature updates while ensuring that large breaking changes are not installed.

This package has a few dependencies:

* Python 3.4 or above, or compatible such as Pypy3.
* A modern (>3.2) version of the ``pymongo`` package and a capable MongoDB 3.4 or newer server.
* A small nubmer of direct Python package dependencies; see the ``setup.py`` file for details.

Additional instructions on `conditional dependencies, package flags, and development version utilization
<https://contentment.webcore.io/installation.html>`__ are available in the manual.


Version History
===============

To see the complete version history, including detailed per-version change logs, please see the `GitHub Releases
<https://github.com/marrow/contentment/releases/latest>`__ section.


License
=======

Contentment has been released under the MIT Open Source license.

The MIT License
---------------

Copyright © 2010-2017 Alice Bevan-McGregor and contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. |ghwatch| image:: https://img.shields.io/github/watchers/marrow/contentment.svg?style=social&label=Watch
    :target: https://github.com/marrow/contentment/subscription
    :alt: Subscribe to project activity on Github.

.. |ghstar| image:: https://img.shields.io/github/stars/marrow/contentment.svg?style=social&label=Star
    :target: https://github.com/marrow/contentment/subscription
    :alt: Star this project on Github.

.. |ghfork| image:: https://img.shields.io/github/forks/marrow/contentment.svg?style=social&label=Fork
    :target: https://github.com/marrow/contentment/fork
    :alt: Fork this project on Github.

.. |masterstatus| image:: http://img.shields.io/travis/marrow/contentment/master.svg?style=flat
    :target: https://travis-ci.org/marrow/contentment/branches
    :alt: Release build status.

.. |mastercover| image:: http://img.shields.io/codecov/c/github/marrow/contentment/master.svg?style=flat
    :target: https://codecov.io/github/marrow/contentment?branch=master
    :alt: Release test coverage.

.. |masterreq| image:: https://img.shields.io/requires/github/marrow/contentment.svg
    :target: https://requires.io/github/marrow/contentment/requirements/?branch=master
    :alt: Status of release dependencies.

.. |developstatus| image:: http://img.shields.io/travis/marrow/contentment/develop.svg?style=flat
    :target: https://travis-ci.org/marrow/contentment/branches
    :alt: Development build status.

.. |developcover| image:: http://img.shields.io/codecov/c/github/marrow/contentment/develop.svg?style=flat
    :target: https://codecov.io/github/marrow/contentment?branch=develop
    :alt: Development test coverage.

.. |developreq| image:: https://img.shields.io/requires/github/marrow/contentment.svg
    :target: https://requires.io/github/marrow/contentment/requirements/?branch=develop
    :alt: Status of development dependencies.

.. |issuecount| image:: http://img.shields.io/github/issues-raw/marrow/contentment.svg?style=flat
    :target: https://github.com/marrow/contentment/issues
    :alt: Github Issues

.. |ghsince| image:: https://img.shields.io/github/commits-since/marrow/contentment/3.0.0.svg
    :target: https://github.com/marrow/contentment/commits/develop
    :alt: Changes since last release.

.. |ghtag| image:: https://img.shields.io/github/tag/marrow/contentment.svg
    :target: https://github.com/marrow/contentment/tree/3.0.0
    :alt: Latest Github tagged release.

.. |latestversion| image:: http://img.shields.io/pypi/v/marrow.mongo.svg?style=flat
    :target: https://pypi.python.org/pypi/Contentment
    :alt: Latest released version.

.. |masterhealth| image:: https://landscape.io/github/marrow/contentment/master/landscape.svg?style=flat
    :target: https://landscape.io/github/marrow/contentment/master
    :alt: Master Branch Code Health

.. |develophealth| image:: https://landscape.io/github/marrow/contentment/develop/landscape.svg?style=flat
    :target: https://landscape.io/github/marrow/contentment/develop
    :alt: Develop Branch Code Health

.. |cake| image:: http://img.shields.io/badge/cake-lie-1b87fb.svg?style=flat
