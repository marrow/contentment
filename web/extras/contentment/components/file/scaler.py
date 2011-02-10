# -*- coding: utf-8 -*-

"""

Base file controller.

"""

import logging
import os
import StringIO

import Image, ImageFile, ImageEnhance

from datetime import datetime
from hashlib import md5


from web.core import config


log = logging.getLogger(__name__)
__all__ = ['cache_hash', 'get_cache', 'save_cache', 'scale']


ImageFile.MAXBLOCK = 1024*1024*40


def cache_hash(*args, **kw):
    log.warn(repr((args, kw)))
    return md5("%r %r" % ( args, kw )).hexdigest()


def get_cache(guid, modified, xy=None, x=None, y=None, square=False, jq=None, style="standard", **kw):
    ihash = cache_hash(guid, modified, xy, x, y, square, jq, **kw)
    if os.path.exists(os.path.join(config['image.cache.path'], guid, ihash + '.jpeg')):
        return os.path.join(config['image.cache.url'], guid, ihash + '.jpeg')
    else: return None


def save_cache(guid, modified, xy=None, x=None, y=None, square=False, jq=None, style="standard", **kw):
    ihash = cache_hash(guid, modified, xy, x, y, square, jq, **kw)
    
    if not os.path.exists(os.path.join(config['image.cache.path'], guid)):
        os.makedirs(os.path.join(config['image.cache.path'], guid))
    
    return os.path.join(config['image.cache.path'], guid, ihash + '.jpeg')


def cache_path(guid, modified, xy=None, x=None, y=None, square=False, jq=None, style="standard", **kw):
    ihash = cache_hash(guid, modified, xy, x, y, sqaure, jq, **kw)
    return os.path.join(config['image.cache.url'], guid, ihash + '.jpeg')


def scale(source, destination, xy=None, x=None, y=None, square=False, jq=None, raw=False, **kw):
    """
    Scale an image from C{source} to the given dimensions and write to C{destination}.
    
    Automatically converts paletted images to truecolor in order to facilitate filtering.
    
    The C{xy} argument is exclusive and can not be used with the C{x} or C{y} arguments.  C{x} and C{y} can be used simultaneously.
    
    @type   source: basestring or file
    @param  source: The path to the source image to scale.
    
    @type   destination: basestring or file
    @param  destination: The path to save the desired scale into.  Parent directories will not be created.
    
    @type   xy: int
    @param  xy: Scale the image to a given maximum dimension.  The longer side will be equal to this, the other will equal or less.
    
    @type   x: int
    @param  x: Scale the width to the given size.  The height is left variable.
    
    @type   y: int
    @param  y: Scale the height to the given size.  The width is left variable.
    
    @type   square: bool
    @param  square: Crop the resulting scaled image to the square center.
    
    @type   jq: int
    @param  jq: JPEG quality expressed as a number between zero and 100.  The default is 95, unless the largest side is smaller than 1024 whereupon a formula will be used to vary the quality between 60 and 95 based on the size of the image.
    
    @type   kw: dict
    @param  kw: Additional arguments are passed directly to the C{Image.save} method when writing the scaled image to disk.
    
    @return: This function returns nothing.
    """
    
    image = Image.open(source)
    
    if image.mode not in ["RGB", "RGBA"]:
        image = image.convert('RGB')
    
    w, h = image.size
    factor = 1
    
    if square:
        l, t = (w / 2) - (min(w, h) / 2), (h / 2) - (min(w, h) / 2)
        image = image.crop((l, t, l + min(w, h), t + min(w, h)))
        w = h = min(w, h)
    
    if x and factor > int(x) / float(w): factor = int(x) / float(w)
    if y and factor > int(y) / float(h): factor = int(y) / float(h)
    if xy: factor = int(xy) / float(max([w, h]))
    
    if factor >= 1:
        if raw: return image, jq if jq else 95
        image.save(destination, "JPEG", optimize=True, quality=jq if jq else 95, **kw)
        return image, jq if jq else 95
    
    thumb = image.resize((int(w * factor), int(h * factor)), Image.ANTIALIAS)
    
    if factor < 0.75:
        enhancer = ImageEnhance.Sharpness(thumb)
        thumb = enhancer.enhance(2.0 - (factor * 1.333))
    
    if jq is None and max(x, y) < 1024:
        jquality = int(60 + 35 * ( 1024.0 / max(w, h) ))
    
    else:
        jquality = jq if jq else 95
    
    if raw: return thumb, jquality
    
    thumb.save(destination, "JPEG", optimize=True, quality=jquality, **kw)
    
    return thumb, jquality
