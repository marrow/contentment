#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals, print_function

import sys
from marrow.script import describe, annotate, Parser

from concurrent import futures

sys.stdout = sys.stderr


def reindex(verbose=False, quiet=False):
    """Re-index all assets on the site."""
    
    from concurrent import futures
    
    import logging
    from web.extras.contentment.components.asset.model import Asset
    
    log = logging.getLogger(__name__)
    
    if verbose and quiet:
        print("Can't set verbose and quiet simultaneously.")
        return 1
    
    num = len(Asset.objects)
    print("Enqueuing %d of %d...\r" % (0, num))
    
    def do(asset):
        try:
            asset = Asset.objects(id=asset).first()
            if not asset:
                return ''
        
        except:
            return num
        
        if hasattr(asset, 'content') and asset.content is None:
            print("missing content... ", end="")
            asset.content = ''
        
        try:
            asset.reindex()
        
        except:
            return asset.path
        
        asset.save()
        return asset.path
    
    f = []
    
    with futures.ThreadPoolExecutor(max_workers=4) as executor:
        for i, asset in enumerate(Asset.objects.only('id', 'path')):
            print("Enqueuing %d of %d... %s\033[K\r" % (i, num, asset.path), end='')
            
            f.append(executor.submit(do, asset.id))
        
        print()
        
        for i, path in enumerate(futures.as_completed(f)):
            print("Waiting for %d of %d... %s\033[K\r" % (i, num, path.result()), end='')
        
        print()


Parser(reindex)(sys.argv[4:])
