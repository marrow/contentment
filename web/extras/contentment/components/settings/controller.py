# encoding: utf-8

"""Basic settings controller."""

import web

import datetime

import pymongo
import mongoengine
from bson.son import SON

from marrow.util.bunch import Bunch

from web.extras.contentment.api import action, view
from web.extras.contentment.components.asset.controller import AssetController


log = __import__('logging').getLogger(__name__)
__all__ = ['SettingsController']



def mintime(time):
    """Accepts seconds, returns a string describing the time span."""
    
    _ = time
    
    if _ < 60: return "<em>%d</em> second%s" % (_, "" if _ == 1 else "s")
    
    __ = _ % 60
    _ = _ // 60
    
    if _ < 60: return "<em>%d</em> minute%s, <em>%d</em> second%s" % (_, "" if _ == 1 else "s", __, "" if __ == 1 else "s")
    
    ___ = __
    __ = _ % 60
    _ = _ // 60
    
    if _ < 24: return "<em>%d</em> hour%s, <em>%d</em> minute%s, <em>%d</em> second%s" % (_, "" if _ == 1 else "s", __, "" if __ == 1 else "s", ___, "" if ___ == 1 else "s")
    
    ____ = ___
    ___ = __
    __ = _ % 24
    _ = _ // 24
    
    if _ < 7: return "<em>%d</em> day%s, <em>%d</em> hour%s, <em>%d</em> minute%s, <em>%d</em> second%s" % (_, "" if _ == 1 else "s", __, "" if __ == 1 else "s", ___, "" if ___ == 1 else "s", ____, "" if ____ == 1 else "s")
    
    _____ = ____
    ____ = ___
    ___ = __
    __ = _ % 7
    _ = _ // 7
    
    if _ < 56: return "<em>%d</em> week%s, <em>%d</em> day%s, <em>%d</em> hour%s, <em>%d</em> minute%s, <em>%d</em> second%s" % (_, "" if _ == 1 else "s", __, "" if __ == 1 else "s", ___, "" if ___ == 1 else "s", ____, "" if ____ == 1 else "s", _____, "" if _____ == 1 else "s")
    
    ______ = _____
    _____ = ____
    ____ = ___
    ___ = __
    __ = _ % 56
    _ = _ // 56
    
    return "<em>%d</em> year%s, <em>%d</em> week%s, <em>%d</em> day%s, <em>%d</em> hour%s, <em>%d</em> minute%s, <em>%d</em> second%s" % (_, "" if _ == 1 else "s", __, "" if __ == 1 else "s", ___, "" if ___ == 1 else "s", ____, "" if ____ == 1 else "s", _____, "" if _____ == 1 else "s", ______, "" if ______ == 1 else "s")


class SettingsAPI(web.core.Controller):
    def compact(self):
        try:
            from web.extras.contentment import core
            
            db = core.connection
            
            name = db.name
            connection = db.connection
            
            before = Bunch(db.command("dbStats"))
            before_ = (before.dataSize + before.fileSize + before.indexSize) / 1024.0 / 1024.0
            
            del db
            
            connection.copy_database(name, name + '_comp')
            
            db = connection[name + '_comp']
            during = Bunch(db.command("dbStats"))
            during_ = (during.dataSize + during.fileSize + during.indexSize) / 1024.0 / 1024.0
            
            del db
            
            if during_ > before_:
                connection.drop_database(name + '_comp')
                return 'json:', dict(status=1, message="Compacting would increase size, compact operation cancelled.")
            
            connection.drop_database(name)
            connection.copy_database(name + '_comp', name)
            
            core.connection = db = connection[name]
            
            after = Bunch(db.command("dbStats"))
            after_ = (after.dataSize + after.fileSize + after.indexSize) / 1024.0 / 1024.0
        
        except:
            return 'json:', dict(status=0, message="Unable to compact database.")
        
        return 'json:', dict(status=1, message="Successfully compacted database: %.2f MiB recovered." % (after_ - before_))
    
    def reindex(self):
        return 'json:', dict()


class SettingsController(AssetController):
    api_settings = SettingsAPI()
    
    @view('Database Administration', 'MongoDB database administration.')
    def view_db(self):
        from web.extras.contentment.core import connection as db
        
        now = datetime.datetime.utcnow()
        
        _server = Bunch(db.connection.admin.command('serverStatus'))
        _col = Bunch(db.command("collStats", 'assets'))
        _db = Bunch(db.command("dbStats"))
        
        server = []
        db_ = []
        indexes = []
        
        
        server.append(('Server Version', u"<em>%s</em> (<em id=\"architecture\">%d</em> bit, latest is <em id=\"latest-version\">…</em>)" % (_server.version, _server.mem.bits, )))
        server.append(('Server Uptime', mintime(_server.uptime)))
        server.append(('Memory Usage', "<em>%d MiB</em> resident, <em>%d MiB</em> virtual, <em>%d MiB</em> mapped" % (_server.mem.resident, _server.mem.virtual, _server.mem.mapped)))
        server.append(('Connections', "<em>%d</em> active connection%s, <em>%d</em> available" % (_server.connections.current, "" if _server.connections.current == 1 else "s", _server.connections.available)))
        server.append(('Storage', '<em>%.2f</em> MiB (~<em>%.2f</em> MiB on-disk) in <em>%d</em> collection%s with <em>%d</em> document%s (<em>%.2f</em> KiB average per document)' % (_db.storageSize / 1024.0 / 1024.0, (_db.dataSize + _db.fileSize + _db.indexSize) / 1024.0 / 1024.0, _db.collections, "" if _db.collections == 1 else "s", _db.objects, "" if _db.objects == 1 else "s", _db.avgObjSize / 1024.0)))
        # server.append(('', ''))
        
        
        db_.append(('Name', "<em>%s</em>" % (db.name, )))
        db_.append(('Overview', '<em>%.2f</em> MiB in <em>%d</em> collection%s with <em>%d</em> document%s (<em>%.2f</em> KiB average per document)' % (_db.storageSize / 1024.0 / 1024.0, _db.collections, "" if _db.collections == 1 else "s", _db.objects, "" if _db.objects == 1 else "s", _db.avgObjSize / 1024.0)))
        db_.append(('Data Size', '<em>%.2f</em> MiB' % (_db.dataSize / 1024.0 / 1024.0, )))
        db_.append(('File Size', '<em>%.2f</em> MiB' % (_db.fileSize / 1024.0 / 1024.0, )))
        db_.append(('Index Size', '<em>%.2f</em> KiB in %d index%s' % (_db.indexSize / 1024.0, _db.indexes, "" if _db.indexes == 1 else "s")))
        db_.append(('Assets', '<em>%.2f</em> KiB in <em>%d</em> asset%s (<em>%.2f</em> KiB average per asset)' % (_col.size / 1024.0, _col.count, "" if _col.count == 1 else "s", _col.avgObjSize / 1024.0)))
        db_.append(('Collections', db.collection_names()))
        # db_.append(('', ''))
        
        
        for i, j in _col.indexSizes.iteritems():
            indexes.append((i, "(<em>%-.2f</em> KiB)" % (j / 1024.0, )))
        
        # indexes.append(('', ''))
        
        
        return 'db', dict(now=now, dbserver=server, db=db_, indexes=indexes)
    
    def api_latest_mongo(self):
        @web.core.cache.cache('admin.mongo.version', expires=86400)
        def cached():
            import urllib
            page = urllib.urlopen('http://www.mongodb.org/downloads')
            return page.read()
        
        return cached()
    
    
