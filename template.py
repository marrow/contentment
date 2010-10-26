# encoding: utf-8

from datetime import datetime

from hashlib import sha512

from web.extras.contentment.components.asset.model import db
from web.extras.contentment.components.asset.model import *
from web.extras.contentment.components.folder.model import Folder
from web.extras.contentment.components.page.model import Page
from web.extras.contentment.components.event.model import Event, EventContact
from web.extras.contentment.components.identity.model import PasswordCredential, Identity
from web.extras.contentment.components.authenticator.model import Authenticator
from web.extras.contentment.components.settings.model import Settings
from web.extras.contentment.themes.default.model import DefaultTheme

conn = db.connect('cms')

Asset.drop_collection()


root = Asset(name="", title="Contentment", default="default", immutable=True, properties={
        'org-contentment-formats-date': '%B %e, %G at %H:%M:%S',
        'org-contentment-theme': 'web.extras.contentment.themes.default',
        'org-contentment-option-attribution': False,
        'org-contentment-option-showdates': True,
        'org-contentment-lang': 'en',
        'org-contentment-cache': True
    }) ; root.save()

admin = Identity(name="admin", title="Administrator", email="webmaster@example.com") ; admin.save()
user = Identity(name="jrh", title="Example User", email="webuser@example.com") ; user.save()


root.acl.append(AdvancedACLRule(allow=False, permission="action:delete", attributes={'immutable': True}))

root.acl.append(OwnerACLRule(allow=True, permission="*"))
root.acl.append(UserACLRule(allow=True, permission="*", reference=admin))

root.acl.append(InheritACLRules()) # child asset rules get inserted here. We want ^ to always take presidence.

root.acl.append(AllUsersACLRule(allow=False, permission="view:acl"))
root.acl.append(AllUsersACLRule(allow=True, permission="view:*"))

root.acl.append(AllUsersACLRule(allow=False, permission="*"))

root.save()


theme = DefaultTheme(name="theme", title="Default Theme", immutable=True); theme.save() ; theme.attach(root)
users = Authenticator(name="users", title="Users", immutable=True) ; users.save() ; users.attach(root)

events = Folder(name="events", title="Events") ; events.save() ; events.attach(root)

settings = Settings(name="settings", title="Site Settings", immutable=True) ; settings.save() ; settings.attach(root)
extensions = Folder(name="extensions", title="Site Extensions", immutable=True) ; extensions.save() ; extensions.attach(settings)
templates = Folder(name="templates", title="Site Templates", immutable=True) ; templates.save() ; templates.attach(settings)

settings.acl.append(UserACLRule(allow=False, permission="*", inverse=True, reference=admin))
settings.save()


admin.attach(users)
user.attach(users)

password = PasswordCredential(identity="admin")
password.password = 'admin'

admin.credentials.append(password) ; admin.save()

password = PasswordCredential(identity="jrh")
password.password = 'jrh'

user.credentials.append(password) ; user.save()


header = Page(name="header", title="Global Site Header", content="""h1. "Contentment":/""")

header.save() ; header.attach(templates)

menu = Page(name="menu", title="Main Menu", engine="raw", content="""
<menu class="container">
    <li class="nav-home"><a href="/">Home<br><label>&nbsp;</label></a></li
    ><li class="nav-start"><a href="/start">Get Started<br><label>Getting Started with Contentment</label></a></li>
</menu>
""")

menu.save() ; menu.attach(templates)

footer = Page(name="footer", title="Global Site Footer", engine="raw", content=u"""<p class="fr">© 2010 Alice Bevan-McGregor</p>

<menu>
    <li><a href="/about">About the Site</a></li
    ><li><a href="/about/privacy">Privacy Policy</a></li
    ><li><a href="/about/colophon">Colophon</a></li>
</menu>
""")

footer.save() ; footer.attach(templates)


custom = Folder(name="custom", title="Custom Page Templates", immutable=True) ; custom.save() ; custom.attach(templates)


default = Page(name="default", title="Welcome", content="""h1. Welcome to Contentment

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""")

default.save() ; default.attach(root)
