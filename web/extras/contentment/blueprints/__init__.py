# encoding: utf-8

from __future__ import unicode_literals, print_function

import datetime
import mongoengine

from marrow.util.bunch import Bunch
from marrow.util.convert import boolean
from marrow.blueprint.api import Blueprint, Folder, File, Setting


__all__ = ['ConfigurationBlueprint', 'SiteBlueprint', 'ComponentBlueprint', 'ThemeBlueprint']



class ConfigurationBlueprint(Blueprint):
    """Configration of a pure Contentment site."""
    
    base = 'web.extras.contentment.blueprints/config'
    inherits = None
    engine = 'mako'
    
    settings = [
            Setting('name', "Configuration Name", "The filename you wish to save the configuration to, must end with '.ini'.", required=True, validator=lambda v: '.ini' in v),
            Setting('develop', "Enable Development Mode", "Enabling development increases the logging level and enables in-browser exception reporting.", values=['y', 'n'], cast=boolean, default='n'),
            Setting('method', "Deployment Method", "FastCGI deployment requires the installation of the 'flup' package.", values=['http', 'fastcgi', 'modwsgi'], default='http'),
            Setting('socket.kind', "Socket Type", values=['port', 'unix'], condition=lambda s: s.method in ['http', 'fastcgi'], default='port'),
            Setting('socket.interface', "Socket Interface", "The IP address to bind to; e.g. '127.0.0.1'.", condition=lambda s: s['socket.kind'] == 'port', default="0.0.0.0"),
            Setting('socket.port', "Port Number", condition=lambda s: s['socket.kind'] == 'port', cast=int, default=8080),
            Setting('socket.path', "Socket Path", "The path to the on-disk UNIX domain socket.", required=True, condition=lambda s: s['socket.kind'] == 'unix'),
            Setting('db', "Database Connection", "Must begin with 'mongo://'.", validator=lambda v: v.startswith('mongo://'), default="mongo://localhost/cms"),
            Setting('static.path', "Static File Path", "The path to serve static files from, e.g. generated image scales.", default="./static"),
            Setting('data.path', "Data File Path", "The path to store session and cache files in.", default="./data")
        ]
    
    manifest = [
            File(lambda s: s.name, 'template.ini'),
            Folder(lambda s: s['static.path']),
            Folder(lambda s: s['data.path'], children=[
                    Folder('cache'),
                    Folder('sessions'),
                    Folder('locks')
                ])
        ]



def mock(settings):
    return dict(settings=Bunch({
            'data.path': './data',
            'db': settings.db,
            'develop': True,
            'method': 'http',
            'name': 'development.ini',
            'socket.interface': '127.0.0.1',
            'socket.kind': 'port',
            'socket.port': 8080,
            'static.path': './static'
        }))

class SiteBlueprint(Blueprint):
    """Configration of a pure Contentment site."""
    
    base = 'web.extras.contentment.blueprints/site'
    inherits = None
    engine = 'mako'
    
    settings = [
            Setting('title', "Site Title", required=True),
            Setting('db', "Database Connection", "Must begin with 'mongo://'.", validator=lambda v: v.startswith('mongo://'), default="mongo://localhost/cms"),
            Setting('admin.name', "Administrative User", default="admin"),
            Setting('admin.title', "Administrative Name", default="Site Administrator"),
            Setting('admin.email', "Administrative E-Mail", required=True),
            Setting('admin.password', "Administrative Password", required=True, hidden=True),
        ]
    
    manifest = [
            File('development.ini', '../config/template.ini', data=mock),
            Folder('static'),
            Folder('data', children=[
                    Folder('cache'),
                    Folder('sessions'),
                    Folder('locks')
                ])
        ]
    
    def post(self):
        print("Bootstrapping default site content...")
        
        from web.extras.contentment.components.asset.model import db, Asset, AdvancedACLRule, OwnerACLRule, UserACLRule, AllUsersACLRule, InheritACLRules
        from web.extras.contentment.components.page.model import Page
        from web.extras.contentment.components.folder.model import Folder
        from web.extras.contentment.components.identity.model import PasswordCredential, Identity
        from web.extras.contentment.components.authenticator.model import Authenticator
        from web.extras.contentment.components.search.model import Search
        from web.extras.contentment.components.settings.model import Settings
        from web.extras.contentment.themes.default.model import DefaultTheme
        
        settings = self.options
        
        scheme, parts = settings.db.split('://', 1)
        parts, db = parts.split('/', 1)
        auth, host = parts.split('@', 1) if '@' in parts else (None, parts)
        
        connection = dict()
        connection['host'], connection['port'] = host.split(':') if ':' in host else (host, '27017')
        connection['port'] = int(connection['port'])
        
        if auth:
            connection['username'], _, connection['password'] = auth.partition(':')
        
        mongoengine.connect(db, **connection)
        
        if Asset.objects().count() > 0:
            print("Existing content found, bootstrap cancelled.")
            # TODO: Interactively ask to overwrite data.
            return
        
        root = Asset(name="", path="/", title=settings['title'], default="default", immutable=True, properties={
                'org-contentment-formats-date': '%B %e, %G at %H:%M:%S',
                'org-contentment-theme': 'web.extras.contentment.themes.default',
                'org-contentment-option-attribution': True,
                'org-contentment-option-showdates': True,
                'org-contentment-lang': 'en',
                'org-contentment-cache': True
            })
        
        admin = Identity(name=settings['admin.name'], title=settings['admin.title'], email=settings['admin.email']) ; admin.save()
        
        root.acl.append(AdvancedACLRule(allow=False, permission="action:delete", attributes={'immutable': True}))
        root.acl.append(OwnerACLRule(allow=True, permission="*"))
        root.acl.append(UserACLRule(allow=True, permission="*", reference=admin))
        root.acl.append(AllUsersACLRule(allow=False, permission="view:acl"))
        root.acl.append(InheritACLRules())
        root.acl.append(AllUsersACLRule(allow=True, permission="view:*"))
        root.acl.append(AllUsersACLRule(allow=False, permission="*"))
        
        root.save()
        
        
        settings_ = Settings(name="settings", title="Site Settings", immutable=True)
        settings_.acl.append(UserACLRule(allow=False, permission="*", inverse=True, reference=admin))
        settings_.save() ; settings_.attach(root)
        
        extensions = Folder(name="extensions", title="Site Extensions", immutable=True) ; extensions.save() ; extensions.attach(settings_)
        templates = Folder(name="templates", title="Site Templates", immutable=True) ; templates.save() ; templates.attach(settings_)
        custom = Folder(name="custom", title="Custom Page Templates", immutable=True) ; custom.save() ; custom.attach(templates)
        
        theme = DefaultTheme(name="theme", title="Default Theme", immutable=True); theme.save() ; theme.attach(root)
        
        users = Authenticator(name="users", title="Users", immutable=True)
        users.acl.append(AllUsersACLRule(allow=True, permission="action:authenticate"))
        users.acl.append(AllUsersACLRule(allow=True, permission="action:expire"))
        users.save() ; users.attach(root)
        
        password = PasswordCredential(identity=settings['admin.name'])
        password.password = settings['admin.password']
        admin.credentials.append(password) ; admin.save() ; admin.attach(users)
        
        header = Page(name="header", title="Global Site Header", content="""h1. "%s":/""" % (settings['title'], )) ; header.save() ; header.attach(templates)
        
        menu = Page(name="menu", title="Main Menu", engine="raw", content="""
<menu class="container">
    <li class="nav-default"><a href="/">Home<br><label>&nbsp;</label></a></li
    ><li class="nav-start"><a href="/start">Get Started<br><label>Getting Started with Contentment</label></a></li>
</menu>""") ; menu.save() ; menu.attach(templates)
        
        footer = Page(name="footer", title="Global Site Footer", engine="raw", content="""<p class="fr">© %s %s</p>

<menu>
    <li><a href="/about">About the Site</a></li
    ><li><a href="/about/privacy">Privacy Policy</a></li
    ><li><a href="/about/colophon">Colophon</a></li>
</menu>""" % (datetime.datetime.now().year, settings['admin.title'])) ; footer.save() ; footer.attach(templates)
        
        search = Search(name="search", title="Site Search") ; search.save() ; search.attach(root)
        
        default = Page(name="default", title="Welcome", owner=admin, content="""h1. Welcome to Contentment

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
) ; default.save() ; default.attach(root)
        
        print("Finished bootstrapping the default site.")
