import web

from datetime                                   import datetime

from web.utils.object                           import CounterMeta
from web.utils.dictionary                       import adict
from web.extras.cmf                             import model as db

from sqlalchemy                                 import func, or_, and_



log = __import__('logging').getLogger(__name__)


# TODO: Split this into a separate decorator.
cache = """
def cache():
    # Determine the latest creation/modification time.
    # TODO: Otptimize this to return a single value from the query rather than an object.
    if scope == "asset":
        latest = max([self.asset.modified if self.asset.modified else datetime(1984, 9, 21), self.asset.created if self.asset.created else datetime(1984, 9, 21)])
        
    else:
        latest = getattr(self.asset, scope)
        latest = latest.order_by(func.if_(Asset.modified > Asset.created, Asset.modified, Asset.created).desc()).first()
        latest = max([latest.modified if latest.modified else datetime(1984, 9, 21), latest.created if latest.created else datetime(1984, 9, 21)])
    
    # Get a canonicalized set of arguments.
    hashable = [(i, j) for i, j in kw.iteritems()]
    hashable.sort()
    hashable = tuple([self.asset.id, scope, latest] + list(args) + hashable)
    
    log.debug("Cache hashable: %r", hashable)
    
    def createfunc():
        log.debug("Cache invalid or non-existant for %r, generating.", self.asset)
        return fn(self, *args, **kw)
    
    result = viewcache.get_value(key=hashable, createfunc=createfunc, expiretime=cache)
    if isinstance(result, dict): result.update(cmf=cmf_namespace, asset=self.asset, controller=self)
    return result"""


class BaseDecorator(object):
    """Code comon to both action and view decorators."""
    
    __metaclass__ = CounterMeta
    
    def __init__(self, name, description=None, icon=None, cache=None, scope="asset"):
        """Pass the decorator the short name (used for path construction), description, and a few optional values:

        `description` -- A human-readable short description.  Will default to the first line of the docstring.
        `icon` -- An icon to represent this view in pretty lists."""
        
        # self.cls = cls
        self.name = name
        self.description = description
        self.icon = icon
        self.cache = (cache, scope)
    
    def prepare(self, controller):
        cmf_namespace = adict(web.extras.cmf.core.namespace)
        cmf_namespace.root = db.session.query(db.Asset).filter_by(l=1).one()
        # cmf_namespace.flash = AttrDict(dict(status=tg.get_status(), message=tg.get_flash())) if tg.get_flash() else AttrDict()
        
        """
        query = db.session.query(db.Extension).filter(
                db.Extension.published <= func.now()
            ).filter(
                or_(
                        db.Extension.retracted == None,
                        db.Extension.retracted >= func.now()
                    )
            )
        """
        
        query = []
        for extension in query:
            log.debug("Processing extension %r for request.", extension)
            ec = extension.controller
            
            if hasattr(ec, 'namespace'):
                log.debug("Extension has namespace components.")
                cmf_namespace.update(ec.namespace)
            
            if hasattr(ec, 'inject'):
                log.debug("Extension has ToscaWidgets injection components.")
                ec.inject(controller)
            
            if hasattr(ec, 'template'):
                log.debug("Extension has Genshi template components.")
                if not isinstance(cmf_namespace.master, list): cmf_namespace.master = [cmf_namespace.master]
                if dotted.get_dotted_filename(ec.template) not in cmf_namespace.master: cmf_namespace.master.append(dotted.get_dotted_filename(ec.template))
        
        return cmf_namespace
    
    def __call__(self, fn):
        pself = self
        
        def wrapper(self, *args, **kw):
            cmf_namespace = pself.prepare(self)
            
            result = fn(self, *args, **kw)
            
            if isinstance(result, tuple):
                result[1].update(cmf=cmf_namespace, asset=self.asset, controller=self)
            
            return result
        
        # Become more transparent.
        wrapper.__name__   = fn.__name__
        wrapper.__doc__    = fn.__doc__
        wrapper.__dict__   = fn.__dict__
        wrapper.__module__ = fn.__module__
            
        wrapper.kind = self.kind, self.name, self.description if self.description else getattr(fn, '__doc__', None), self.icon
        wrapper._counter = self._counter
        
        return wrapper


class view(BaseDecorator):
    kind = 'view'

class action(BaseDecorator):
    kind = 'action'
