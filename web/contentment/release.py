# encoding: utf-8

"""Release information about Contentment."""

from __future__ import unicode_literals

import sys
from collections import namedtuple


version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel', 'serial'))(3, 0, 0, 'alpha', 1)
version = ".".join([str(i) for i in version_info[:3]]) + ((version_info.releaselevel[0] + str(version_info.serial)) if version_info.releaselevel != 'final' else '')

author = namedtuple('Author', ['name', 'email'])("Alice Bevan-McGregor", 'alice@gothcandy.com')
description = "A component management system that excels at managing content."
copyright = "2009-2015, Alice Bevan-McGregor and contributors"
url = 'https://github.com/marrow/Contentment/'
