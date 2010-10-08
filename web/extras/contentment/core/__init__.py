import pkg_resources

from marrow.util.bunch import Bunch

from web.extras.cmf.core.decorators import action, view



__all__ = ['components', 'action', 'api', 'view', 'Action', 'View']
log = __import__('logging').getLogger(__name__)



components = adict()
namespace = adict()


# namespace.master = [dotted.get_dotted_filename(config.master)] if config.get('master', None) else []

for res in pkg_resources.iter_entry_points('contentment.component'):
    try:
        instance = res.load()
        
        if callable(instance):
            instance = instance()
        
        log.debug("%r: %r", instance, dir(instance))
    
    except:
        log.exception("Error scanning available CMF components.  CMF unavailable.")
        break
    
    try:
        if hasattr(instance, 'enabled'):
            if hasattr(instance, 'start') and callable(instance.start):
                instance.start()
            
            components[res.name] = instance
    
    except:
        log.exception("Error initializing CMF component %r.", instance)
        continue

log.info("Loaded CMF components: %s", ', '.join([i.title for i in components.itervalues()]))
