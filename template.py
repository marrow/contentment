# encoding: utf-8

from hashlib import sha512

from web.extras.contentment.components.asset.model import Asset, db
from web.extras.contentment.components.folder.model import Folder
from web.extras.contentment.components.page.model import Page
from web.extras.contentment.components.identity.model import PasswordCredential, Identity
from web.extras.contentment.themes.default.model import DefaultTheme

conn = db.connect('cms')

Asset.drop_collection()


root = Asset(name="", title="Contentment", default="default", properties={
        'org-contentment-formats-date': '%B %e, %G at %H:%M:%S',
        'org-contentment-theme': 'web.extras.contentment.themes.default',
        'org-contentment-option-attribution': False,
        'org-contentment-option-showdates': True,
        'org-contentment-lang': 'en',
        'org-contentment-cache': True
    }) ; root.save()

theme = DefaultTheme(name="theme", title="Default Theme"); theme.save() ; theme.attach(root)
extensions = Folder(name="extensions", title="Site Extensions") ; extensions.save() ; extensions.attach(root)
templates = Folder(name="templates", title="Site Templates") ; templates.save() ; templates.attach(root)
users = Folder(name="users", title="Users") ; users.save() ; users.attach(root)


admin = Identity(name="admin", title="Administrator", email="webmaster@example.com")
admin.save()
admin.attach(users)

password = PasswordCredential(identity="admin")
password.password = 'admin'

admin.credentials.append(password)
admin.save()


header = Page(name="header", title="Global Site Header", content="""h1. "Contentment":/""")

header.save() ; header.attach(templates)

menu = Page(name="menu", title="Main Menu", engine="raw", content="""
<menu class="container">
    <li class="nav-home"><a href="/">Home<br><label>&nbsp;</label></a></li
    ><li class="nav-start"><a href="/start">Get Started<br><label>Deployment Options</label></a></li
    ><li class="nav-faq"><a href="/faq">FAQ<br><label>Frequently Asked Questions</label></a></li
    ><li class="nav-news"><a href="/news/">News<br><label>Latest News</label></a></li
    ><li class="nav-contact"><a href="/contact">Contact<br><label>Contact MVP</label></a></li
    ><li class="nav-features"><a href="/features">Features<br><label>What MVP Does</label></a></li>
</menu>
""")

menu.save() ; menu.attach(templates)

footer = Page(name="footer", title="Global Site Footer", content=u"""p(fr). © 2010 Alice Bevan-McGregor

- "About the Site":/about/
- "Privacy Policy":/about/privacy
""")

footer.save() ; footer.attach(templates)


custom = Folder(name="custom", title="Custom Page Templates") ; custom.save() ; custom.attach(templates)


default = Page(name="default", title="Welcome", content="""h1. Welcome to Contentment

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""")

default.save() ; default.attach(root)
