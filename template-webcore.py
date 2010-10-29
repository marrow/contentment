# encoding: utf-8

from template import root, header, menu, footer, default, admin

from web.extras.contentment.components.asset.model import db
from web.extras.contentment.components.asset.model import *
from web.extras.contentment.components.folder.model import Folder
from web.extras.contentment.components.page.model import Page
from web.extras.contentment.components.alias.model import Alias
from web.extras.contentment.components.identity.model import PasswordCredential, Identity
from web.extras.contentment.components.authenticator.model import Authenticator
from web.extras.contentment.components.search.model import Search
from web.extras.contentment.components.settings.model import Settings
from web.extras.contentment.themes.default.model import DefaultTheme


root.title = "WebCore"
root.save()

admin.title = "Alice Bevan-McGregor"
admin.credentials[0].password = ""
admin.save()


header.content = u"""h1. "WebCore":/

p{margin-left: 10px; color:white; margin-bottom: 0}. A lightweight and extremely fast Python web framework.""" ; header.save()

menu.content = u"""<menu>
    <li class="nav-home"><a href="/">Home<br><label> </label></a></li
    ><li class="nav-features"><a href="/features">Features<br><label>Core and Unique Features</label></a></li
    ><li class="nav-download"><a href="/download">Download<br><label>Downloading and Installing</label></a></li
    ><li class="nav-documentation"><a href="/docs">Documentation<br><label>Manual and Tutorials</label></a></li
    ><li class="nav-community"><a href="/community">Community<br><label>Support and Discussion</label></a></li
    ><li class="nav-wiki"><a href="/wiki/">Wiki<br><label>Community Documentation</label></a></li
></menu>""" ; menu.save()

footer.content = u"""<p class="fr">© 2009–2010 Alice Bevan-McGregor</p>

<menu>
    <li><a href="/about">Colophon</a></li
    ><li><a href="/about/privacy">Privacy Policy</a></li
></menu>""" ; footer.save()


default.content = u"""h1(primary). Welcome to WebCore

|_>. Who’s going to use it? | Software developers seeking to write fast, maintainable code. |
|_>. How does it look? | Clean and efficient, with almost zero code overhead and excellent documentation. |
|_>. What does it do? | For a full list of features, see the "Features":/Features page. |

h2. "Full Stack" Component Architecture

* *Databases*: "SQLAlchemy":http://www.sqlalchemy.org/, "MongoDB":http://www.mongodb.org/, and easily extendable to others.
* *Templating*: Genshi, Jinja2, Python Templates, and more, also easily extendable.
* *Serialization*: JSON, YAML, Bencode, Python Pickle, &c.
* *Dialects*: Object dispatch, Routes, XML-RPC, Flash AMF, or roll your own.
* *Extras*: WebAuth, ToscaWidgets, Beaker sessions and caching, and any WSGI middleware you can find.

h2. Easy to Use

Simple applications are easy to get up and running.

pre(gist#240887). See Gist #240887 (http://gist.github.com/240887) on GitHub.""" ; default.save()


about = Folder(name="about", title="About", owner=admin, default="default") ; about.save() ; about.attach(root)

_ = Page(name="default", title="About the Site", owner=admin, content=u"""h1(primary). About the WebCore Website

The WebCore website is powered by the "Contentment":http://github.com/GothAlice/Contentment content management system, the "WebCore":http://www.web-core.org/ web application development framework, and "Python":http://www.python.org/, a high-level general purpose scripting language.

Portions of the code are copyright their respective authors and distributed under various licenses.  For more information, please see the specific project websites and respective dependant packages.

p(tc). Developed by "Alice Bevan-McGregor":http://www.gothcandy.com/

p(tc). Contentment Copyright © 2010 Alice Bevan-McGregor
WebCore Copyright © 2009-2010 Alice Bevan-McGregor, Alex Grönholm, and Contributors
Python Copyright © 1990-2010 Python Software Foundation""") ; _.save() ; _.attach(about)

_ = Page(name="privacy", title="Privacy Policy", owner=admin, description=u"This privacy policy sets out how WebCore uses and protects any information that you voluntarily or involuntarily provide when you use this website.", content=u"""h1(primary). WebCore Privacy Policy

WebCore is committed to ensuring that your privacy is protected. Should we ask you to provide certain information by which you can be identified when using this website, then you can be assured that it will only be used in accordance with this privacy statement.

WebCore may change this policy from time to time by updating this page. You should check this page from time to time to ensure that you are happy with any changes. The date this policy was last modified is available in the footer. (You can hover your mouse over the relative date to view the absolute one.)

bq. This privacy policy sets out how WebCore uses and protects any information that you voluntarily or involuntarily provide when you use this website.

h1. What We Collect

We may collect the following information:

* Your name,
* Contact information including email address,
* Information as required to fulfill orders placed through the site, and,
* Other information relevant to customer surveys and/or offers.

h1. What We do With the Information We Gather

We require this information to understand your needs and provide you with a better service, and in particular for the following reasons:

* Internal record keeping.
* Anonymous trend and site usage monitoring.
* We may use the information to improve our products and services.
* We may use the information to customise the website according to your interests.

h1. Security

We are committed to ensuring that your information is secure. In order to prevent unauthorised access or disclosure we have put in place suitable physical, electronic and managerial procedures to safeguard and secure the information we collect online.

h1. How We use Cookies

A cookie is a small section of data stored by a website on your computer, only accessible by the site who initially saved the cookie. Use of cookies is limited on this site. We primarily use cookies to track and grant authenticated access to restricted areas of the site and shopping cart sessions. All cookieson this site are configured to expire after a small time period; we do not store information permanently on your computer.

Our third-party partners, such as Google Analytics, may use traffic log cookies to identify which pages are being used. This helps us analyse data about webpage traffic and improve our website in order to tailor it to customer needs. We only use this information for statistical analysis purposes and then the data is removed from the system. Additionally, this information is not personally identifiable.

Overall, cookies help us provide you with a better website, by enabling us to monitor which pages you find useful and which you do not. A cookie in no way gives us access to your computer or any information about you, other than the data you choose to share with us.

You can choose to accept or decline cookies. Most web browsers automatically accept cookies, but you can usually modify your browser setting to decline cookies if you prefer. This may prevent you from taking full advantage of the website by, for example, preventing you from accessing password protected areas.

h1. Links to Other Websites

Our website may contain links to other websites of interest. However, once you have used these links to leave our site, you should note that we do not have any control over that other website. Therefore, we cannot be responsible for the protection and privacy of any information which you provide whilst visiting such sites and such sites are not governed by this privacy statement. You should exercise caution and look at the privacy statement applicable to the website in question.

h1. Controlling your Personal Information

You may choose to restrict the collection or use of your personal information in the following ways:

* Whenever you are asked to fill in a form on the website, look for the box that you can click to indicate that you do not want the information to be used by anybody for direct marketing purposes.
* If you have previously agreed to us using your personal information for direct marketing purposes, you may change your mind at any time by writing to or emailing us.* We will not sell, distribute or lease your personal information to third parties unless we have your permission or are required by law to do so. We will not use your personal information to send you promotional information about third parties unless you explicitly tell us that you wish this to happen.

You may request details of personal information which we hold about you under the Data Protection Act of 1998. A small fee will be payable. If you would like a copy of the information held on you please write to [address].

If you believe that any information we are holding on you is incorrect or incomplete, please write to or email us as soon as possible, at the above address. We will promptly correct any information found to be incorrect.""") ; _.save() ; _.attach(about)


_ = Page(name="features", title="Features", owner=admin, content=u"""h1(primary). WebCore Features

* *Extreme performance.* Benchmarked on the same system, WebCore is 2-10 times faster than other frameworks on a bare-bones "Hello World" test, while offering the same core features.

* *Everything you need, out of the box.* Sessions, authentication, database, JSON, internationalization, form generation, templating, and more, without locking you into any given component. _Use as much or as little as you want._

* *Makes complex things easy.* From multiple database connections to dynamic template selection, many of WebCore's features were taken directly from community discussion.

* *Follows the Zen of Python.* WebCore follows all of the guidelines outlined in the "Zen of Python":http://www.python.org/dev/peps/pep-0020/ as closely as possible. This helps everything just make sense.

* *Rapid web _application_ development.* The web has grown to be more complicated than simple HTML pages and forms. WebCore includes alternate dialects for things like XML-RPC and Flash AMF to help you develop powerful applications.

* *Simple applications.* WebCore can host an application as simple as a single file, or as complicated as you like.  (We like setuptools packages, though.)

* *Easy to extend, but already covers a lot.* Using namespaces it's easy to create additions that blend in with the core package.

* *Simple installation with few dependencies.* A full stack (sessions, caching, templating, etc.) installs just 10 packages, a light-weight installation installs just 6.

* *Production quality components.* WebCore is built on top of Paste and WebOb, two of the most widely deployed components for the creation of web frameworks in Python.

h2. Features Unique to WebCore

* *Return any data structure.* From within a controller you can return almost any data structure, and WebCore will work out what you mean.  String, unicode, Response object, file handle, list, generators, and iterables are supported.  (Tuples are used for template selection.)""") ; _.save() ; _.attach(root)


_ = Page(name="download", title="Download", owner=admin, content=u"""h1(primary). Downloading and Installing WebCore

Full installation documentation is "available online":http://packages.python.org/WebCore/, but to get started quickly you will need the following:

# A copy of Python greater than or equal to 2.5, and less than 3.0.
# The "webcore-bootstrap.py":http://www.web-core.org/webcore-bootstrap.py file.

Go to the folder you want to contain the WebCore virtual environment for your web application and run:

pre. python webcore-bootstrap.py --production <name>

Where @<name>@ is the name you wish to give your environment.  If you want to specify a version of Python other than the system default, pass in the additional argument @--python=pythonX.Y@ where @X.Y@ is the version you want to use.  Python Distribute and WebCore will both be automatically downloaded and installed into the new environment.

When everything is ready, feel free to follow one of the "tutorials":http://packages.python.org/WebCore/#tutorials in the documentation, or just "dive right in":http://packages.python.org/WebCore/core/basic/index.html.

h1. Working with the Development Version

If you want to play with the latest and greatest, and potentially slightly unstable API from commit to commit, you can clone our public GitHub repository.

pre. git clone git://github.com/GothAlice/WebCore.git

If you want to make changes, however, you should probably get yourself a GitHub account (if you didn't already have one) and fork a copy for yourself.  Patches are greatly appreciated, but will only be accepted into core if accompanied by unit tests.

h1. What's the scoop?

If you're curious about what goes into each release, you can keep track on the "Changes":/changes page.""") ; _.save() ; _.attach(root)


_ = Alias(name="docs", title="Documentation", owner=admin, target="http://packages.python.org/WebCore/") ; _.save() ; _.attach(root)


_ = Page(name="community", title="Community", owner=admin, content=u"""h1(primary). WebCore Community

h2. Issue Tracking

WebCore currently uses GitHub's "online issue tracker":http://github.com/GothAlice/WebCore/issues to manage support tickets.  If you have a problem you can post an issue there.

h2. Support Chat Room

You can find more immediate support through IRC on "irc.freenode.net":irc://irc.freenode.net:6667/webcore in #webcore.  Look for GothAlice.

h3. IRC Archive

IRC archival software is currently under development.

h2. Mailing List

A preliminary mailing list is available through "Google Groups":http://groups.google.com/group/webcore-devel.  Until the user base grows signifigantly, or Google Group's problems catch up with us, this will be a reasonable place to have long-term discussion.""") ; _.save() ; _.attach(root)


wiki = Folder(name="wiki", title="Wiki", description=u'', owner=admin, default="default", sort="title") ; wiki.save() ; wiki.attach(root)


_ = Page(name="changes", title="Changes", owner=admin, description=u'', content=u"""h1(primary). WebCore Change History

The following is a reverse-chronological listing of the releases with a list of changes for each version in chronological order.

h2. Version 1.0.0

* *New*: A La Carte's TemplateMiddleware has been migrated into @web.extras@ as it is specific to WebCore.
* *Changed*: Now references the @alacarte@ package instead of @cti@.
* *New*: Added i18n functions to global template scope.  This does not effect message extraction, which must be considered when choosing a templating language.
* *New*: Re-usable colophon and useful version_info tuple.
* *Changed*: Simplified by matching argspec and using functools.wrap on the authorize decorator.
* *New*: Added BasicAuthMiddleware care of Alex Grönholm. 
* *Changed*: Various cleanup updates (removal of unnecessary imports, etc.) of the examples and core code.
* *Changed* / *Removed*: Updated documentation, removed parts that should reference external documentation, and added a TODO section.

h2. Version 0.9.0

Nearing a final, stable release comes version *0.9*, featuring:

* *Fixed*: The default SQLAlchemy @pool_recycle@ is now 3600 seconds, resolving "issue #15":http://github.com/GothAlice/WebCore/issues/issue/15. 
* *Changed*: The @force@ argument is no longer passed to the developer-supplied authentication callback function.  Your code may need to be updated to remove this argument.
* *New*: Used the SQLAlchemy transactional middleware as a template for a new generic transactional API, and updated the SA middleware to use this API.
* *Removed*: The constant profiling (@web.extras.cprofile@) middleware has been removed in this version.  It will be re-released in a separate package along with controllers capable of analyzing the data.
* *Changed*: The @web.core.dialects@ module has been split into multiple modules within the new @web.core.dialects package@.
* *Removed*: Import cleanup and removed a Rakefile used for the first attempt at integration testing.
* *Removed*: Unused AuthKit support.  If the demand is there, I can try to create better integration, but as it stands I don't know enough about AuthKit to integrate it properly.
* *Added*: A number of new unit tests, improving overall unit test coverage for a number of modules.
* *Changed*: The RESTMethod dialect now lower-cases the verb no matter the input, @_verb@ @query_string@ override or from HTTP.
* *Added*: Filename extensions are now allowed and are stored in @web.core.request.format@, allowing you to conditionally return based on requested format.  E.g. @data.xml@ vs. @data.json@.
* *Added*: Added compatibility with other frameworks with RESTful dispatch; you can now port code and receive friendly warnings about the use of _method to override the HTTP verb.
* *Added*: Routes-based dispatch.
* *Added*: A new package namespace is available, @web.app@, for you to place your own applications in.  This eliminates the need to pollute the top-level Python package namespace.

h2. Version 0.6.2

This is a critical security release pushed out to correct a potential privilege escalation issue in the WebAuth @authentication@ method.  Specifically, if a user manages to construct malformed data that is capable of producing an exception from within the developer-supplied @authenticate@ callback, or an exception is raised under other circumstances from the same callback, the user will be authenticated regardless of having provided valid credentials or not.  (Only the identifier need be correct.)  This release corrects this behavior.

* *Fixed*: Corrected the security flaw mentioned above.
* *Updated*: Numerous updates to the experimental "Constant Profiling" middleware.
* *Added*: The application configuration is now available in the 'web' template namespace.

h2. Version 0.6.1

This is a bugfix release primarily focused on reversing breaking changes introduced in version 0.6.

* *Fixed*: Fixed a breaking change in the handling of SQLAlchemy thread-local sessions.  (Everything is back to normal now, no change to application code needed.)
* *Fixed*: Fixed SQLAlchemy middleware handling of non-2xx HTTP status codes.

h2. Version 0.6

* *Fixed*: Reduced logging output of SA DB layer to prevent log clutter from missing @favicon.ico@ and @robots.txt@ files.
* *Fixed*: i18n: More careful about using Beaker sessions, in case they aren't available.
* *New*: i18n: `_` function now automatically detects which (of `ugettext` or `ungettext`) should be called depending on the argument count.  There is now also a lazy version available called `L_`.
* *New*: i18n: Made get_translator public.
* *New*: Added more obvious logging to help diagnose issues with badly assigned root controllers.  You -can- use a raw WSGI application as your root controller, it just raises a warning now in case that isn't the desired behaviour.
* *Fixed*: Fix for import errors of the 'http' aliased module.
* *Fixed*: Fixed non-UNIX paths in bootstrap script.
* *Updated*: Fixed double-management of SQLAlchemy sessions. Now relies on SA's native @scoped_session@ and SqlSoup's @objectstore@.
* *Fixed*: Removed the SQLAlchemy middleware's dependancy on WebCore structures; @web.db.sa@ is now WSGI clean.
* *Fixed*: Non-WebCore database middleware can now be loaded by name.

h2. Version 0.5.4

* *Fixed*: Configuration is now assigned to @web.core.config@ before root controller instantiation, allowing you to use it in your application's configuration.

h2. Version 0.5.3

* *New*: Allow overriding of the REST verb for non-RESTful clients by way of the @_verb@ @QUERY_STRING@ argument.
* *Fixed*: (Security) Removed potentially revealing authorization error for private attribute access failthrough.
* *New*: At least partial unit test coverage for the authentication and authorization middleware and predicates.
* *New*: You can now pass in Python callables instead of dot-notation strings for the CoreAuth callbacks, facilitating simple (non-INI) deployment.
* *Fixed*: Armoured the CoreAuth predicates against use of the @web.auth.user@ variable outside standard WSGI requests.
* *New*: Added a localhost REMOTE_USER on all unit test WSGI requests.
* *New*: Extended the object dispatch dialect to support generic callables as return values from @__lookup__@.

h2. Version 0.5.2

* *Fixed*: Corrected off-by-one slicing of the Beaker Cache middleware configuration keys.

h2. Version 0.5.1

* *Fixed*: Corrected a number of issues with the use of the Distribute relocatable and @virtualenv@ bootstrap script generator.
* *Fixed*: Corrected import error of CoreAuth due to missing @has_permission@ predicate, which should never have been there to start.

h2. Version 0.5

* *New*: Initial "preview" release.
* *Breaking*: Earlier (Git master) versions of the Object Dispatch component used @default@ and @lookup@ magic methods to perform advanced dispatch.  These methods have been re-named @__default__@ and @__lookup__@ respectively to clear the namespace for your own code.""") ; _.save() ; _.attach(root)


# _ = Page(name="", title="", owner=admin, content="""""") ; _.save() ; _.attach(root)


news = Folder(name="news", title="News", owner=admin, default="view:details", sort="-created") ; news.save() ; news.attach(root)

# _ = RSS(name="rss", title="RSS Feed", owner=admin, sort="-created") ; _.save() ; _.attach(news)


_ = Page(name="default", title="Welcome to the Wiki", owner=admin, content=u"""h1(primary). Community Wiki

This public wiki (editable by anyone with an account) is a great place to store user-contributed tutorials, recipes for special cases, and topical discussion of specific features or future plans.

h2. Primary Areas

* "Tutorials":/wiki/Tutorials
* "Code Recipes":/wiki/Recipes

h2. Orphaned Sections

The following sections don't belong to a top-level category.

* "Common Problems and Caveats":/wiki/Caveats
* "Why WebCore?":/wiki/WhyWebCore

h2. Meta–Articles

These are articles that describe the functionality of the Wiki.

* "WebCore Wiki Macros":/wiki/WikiMacros
""") ; _.save() ; _.attach(wiki)


_ = Folder(name="Tutorials", title="Tutorials", owner=admin, default="view:details", sort="title") ; _.save() ; _.attach(wiki)


recipes = Folder(name="Recipes", title="Code Recipes", owner=admin, default="view:details", sort="title") ; recipes.save() ; recipes.attach(wiki)
forms = Folder(name="Forms", title="Form Handling", owner=admin, default="view:details", description="Widgets, validation, tips and tricks.", sort="title") ; forms.save() ; forms.attach(recipes)

_ = Page(name="AjaxFileUpload", title="AJAX Multiple File Upload", description="Handle file uploads which process in the backround and display progress to the user.", content=u"""h1(primary). AJAX Multiple File Upload

bq. (the following are my notes thus far)

* using "jquery-html5-upload":http://code.google.com/p/jquery-html5-upload/ or similar that uses @xhr.send(file)@ to send the file in WebKit browsers
* i.e. not using a true @multipart/form-data@ encoding
* using @multipart/form-data@ raises an error when processing the data

to fix:

* don't use @POST@ and @multipart/form-data@, use @PUT@ and @application/octet-stream@ instead -- @POST@ /might/ work with a different encoding, but I don't want to risk it

to use:

* use web.core.request.body (a file like object) to stream the file where you want it to go (mongo, disk, S3, etc.)

benefit:

* doesn't necessarily load entire file into RAM
* streamline user experience without the need for Adobe Flash
* multiple file uploads with progress feedback""") ; _.save() ; _.attach(forms)


_ = Page(name="Caveats", title="Problems and Caveats", owner=admin, content=u"""h1(primary). Common Problems and Caveats

h2. I use caching or otherwise return a zero-length body, and I get this strange traceback...

You are probably using the GzipMiddleware; disable it and your problem should go away.  See "this ticket on Paste's Trac":http://trac.pythonpaste.org/pythonpaste/ticket/318 for more information.""") ; _.save() ; _.attach(wiki)


_ = Page(name="WhyWebCore", title="Why WebCore?", owner=admin, content=u"""h1(primary). Why yet another web framework?

For purely selfish reasons.

I was an avid user and contributor for one of the more popular "Python":http://www.python.org/ web frameworks, "TurboGears":http://www.turbogears.org/, for quite some time. (Mostly as a helpful busybody on IRC, though TurboMail was originally TurboGears-specific.) Many of its features were quite killer, and making use of existing "best of breed" components made sense.

After developing several large applications with it, and grappling with obscure issues, I began to appreciate the fundamental complexity of a framework. Even more, I appreciated the jump from "easy" to "easy to get started with". Some things were hard. Some of the "advanced things":http://trac.turbogears.org/ticket/2291 I tried didn't work. And I couldn't figure out why.

Other things, like multiple database support, "modifying the returned content-type":http://trac.turbogears.org/ticket/2158, and "dynamic selection of templates":http://trac.turbogears.org/ticket/2168 were bizarrely hard to do, and required that you understand and use several bits of magic. Magic is bad.

I tried experimenting with "Web.py":http://www.webpy.org/, but ended up removing 80% of it in "my own fork":http://github.com/GothAlice/webpy/tree. I got tired of ripping and tearing, and decided to write my own best of breed framework using the same underlying components as my favourite to date, TurboGears.

h1. Why not take TurboGears and fix perceived problems?

Code complexity.

When I was dissecting Web.py I discovered rapidly that even for a light-weight framework, it had a lot of inter-dependancies. TurboGears is currently a far more profound stack of explicitly required components:

* Paste
* Pylons
* TurboGears

The actual number of packages installed with a clean, basic install is around 35. This number is aggravated by the fact that each major layer has its own dependancies, and I would have to have the same level of knowledge of all layers as if I had written them myself. I might as well write it myself.

WebCore's install base is around 9 packages; fewer if you don't use certain features in your webapp.

h1. What's so special about WebCore?

Several things. As mentioned above, light-weight dependancies are key. The total amount of code in the framework should be minimal. Performance should be great - all the work should happen in the application you develop. It makes no assumptions about the type of application you are trying to develop. It should be easy to do easy things, and there should be an obvious way to do hard things.""") ; _.save() ; _.attach(wiki)


_ = Page(name="WikiMacros", title="Wiki Macros", owner=admin, content=u"""h1(primary). WebCore Wiki Macros

Wiki macros are implemented in JavaScript where possible to aide in caching of dynamic content.  This does mean, however, that you should provide some sane default value to appear in case JavaScript is disabled or the user is constrained by a slow connection.

h2. GitHub Gist

You can mark any pre-formatted text block (@pre.@) for replacement with a syntax coloured (and version tracked) code block by defining @gist@ as the class and the ID of the Gist as the @#id@.  E.g.

pre. pre(gist#240887). ...
""") ; _.save() ; _.attach(wiki)
