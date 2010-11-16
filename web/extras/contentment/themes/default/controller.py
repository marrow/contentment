# encoding: utf-8

"""Default theme controller."""

from __future__ import with_statement

import os
import sys
import time
import datetime
import mimetypes

import web

from web.extras.contentment.components.theme.controller import ThemeController


log = __import__('logging').getLogger(__name__)
__all__ = ['DefaultThemeController']



class DefaultThemeController(ThemeController):
    pass
