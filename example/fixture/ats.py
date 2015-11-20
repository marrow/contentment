# encoding: utf-8

import logging.config
import cinje

logging.config.dictConfig({
		'version': 1,
		'handlers': {
				'console': {
						'class': 'logging.StreamHandler',
						'formatter': 'json',
						# 'level': 'debug',
						'stream': 'ext://sys.stdout',
					}
			},
		'loggers': {
				'web': {
						'level': 'DEBUG',
						'handlers': ['console'],
						'propagate': False
					},
			},
		'root': {
				'level': 'INFO',
				'handlers': ['console']
			},
		'formatters': {
				'json': {
						'()': 'web.contentment.util.JSONFormatter',
						'format': '%(asctime)s\t%(levelname)s\t%(name)s:%(funcName)s:%(lineno)s  %(message)s',
						# 'force_keys': ('levelname', 'lineno'),
						
					}
			},
		
		
	})




from mongoengine import connect
connect('contentment')

from web.component.asset import Asset
from web.component.page.model import Page
from web.component.page.block.reference import ReferenceBlock
from web.component.page.block.content import TextBlock, DescriptionBlock
from web.component.page.block.map import MapBlock
from web.component.page.block.video import VideoBlock
# from web.component.career import Employment


Asset.drop_collection()
Asset.ensure_indexes()



root = Asset(
		name = '/',
		path = '/careers.illicohodes.com',
		title = dict(en="Careers at Illico Hodes"),
		handler = 'careers',
	)
root.properties.title = dict(separator=': ', direction='ltr')
root.save()


theme = Asset(name='theme', title=dict(en="Site Theme")).save()
root = root.append(theme)

parts = Asset(name='part', title=dict(en="Parts")).save()
theme = theme.append(parts)

images = Asset(name='img', title=dict(en="Images")).save()
theme = theme.append(images)
styles = Asset(name='css', title=dict(en="Styles")).save()
theme = theme.append(styles)
scripts = Asset(name='js', title=dict(en="Scripts")).save()
theme = theme.append(scripts)


_1 = TextBlock(content=dict(en="<h1><a href=\"/\">Careers</a><small> at <a href=\"/\" class=\"logo\">Illico Hodes</a></small></h1>"))
_1.properties.width = 8
_1.properties.id = "logo"
_2 = TextBlock(content=dict(en='<menu class="list-inline"><li><a href="/home">Home</a></li><li><a href="/home#featured">Featured</a></li><li><a href="/home#all">All Jobs</a></li></menu>'))
_2.properties.width = 4
_2.properties.id = "acct-nav"
header = Page(name='header', title=dict(en="Default Page Header"), content = [
		_1, _2,
	]).save()
parts = parts.append(header)

footer = Page(name='footer', title=dict(en="Default Page Footer"), content = [
		TextBlock(content=dict(en='''<p>© 2015 Illico Hodes.</p>

<menu>
<li><a href="/terms">Terms</a></li>
<li><a href="/privacy">Privacy</a></li>
</menu>'''))
	]).save()
parts = parts.append(footer)

aside = Page(name='aside', title=dict(en="Job Detail Aside"), content = [
		TextBlock(content=dict(en='''<h3>Re-Imagine Work</h3>

<p>Donec ullamcorper nulla non metus auctor fringilla. Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit. Donec ullamcorper nulla non metus auctor fringilla. Maecenas faucibus mollis interdum.</p>

<p>Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Nullam id dolor id nibh ultricies vehicula ut id elit. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Curabitur blandit tempus porttitor.</p>

{apply}'''))]).save()
parts.append(aside)



jobs = Page(name='job', title=dict(en="Job Details")).save()
root = root.append(jobs)

_hdr = ReferenceBlock(target=header)
_hdr.properties.cls = 'container-fluid'
_1 = TextBlock(content=dict(en='''<h1>Careers at Illico Hodes</h1>'''))
_1.properties.cls = 'hero-img'
_2 = TextBlock(content=dict(en='''<p>Featured jobs go here.</p>''')) # ReferenceBlock(target=jobs, handler='only_featured')
_2.properties.cls = 'focus'
m1 = MapBlock(query="1765 Fern Road, Courtenay, BC")
m1.properties.width = 6
m2 = MapBlock(query="Montréal, Québec")
m2.properties.width = 6
v1 = VideoBlock(video='ziJ_baa_60A')
v1.properties.width = 8
_3 = TextBlock(content=dict(en='''<p>More text here.</p>'''))
_3.properties.width = 4
careers = Page(name='careers', title=dict(en="Careers at Illico Hodes"), content = [
		_hdr,
		_1,
		_2,
		TextBlock(content=dict(en='''Jobs by category go here.''')),
		m1,
		m2,
		v1,
		_3,
		# ReferenceBlock(target=jobs, handler='by_category'),
		ReferenceBlock(target=footer),
	]).save()
root = root.append(careers)

_0 = ReferenceBlock(target=header)
_0.properties.cls = 'ih-head'
_0.properties.block = 'header'
_1 = TextBlock(content=dict(en='''{job.as_html}'''))
_1.properties.width = 9
_1.properties.id = 'job-detail'
_2 = ReferenceBlock(target=aside)
_2.properties.width = 3
_2.properties.id = 'job-aside'
_4 = TextBlock(content=dict(en='''<h2>{job.title[en]}</h2>'''))
_4.properties.id = 'job-hero'
_5 = DescriptionBlock()
_5.properties.cls = 'job-summary'
_6 = ReferenceBlock(target=footer)
_6.properties.block = 'footer'
job = Page(name='_template', title=dict(en="{job.title[en]}"), content = [
		_0,
		_4,
		_5,
		_1,
		_2,
		_6,
	]).save()
jobs = jobs.append(job)



terms = Page(name='terms', title=dict(en="Terms of Service"), content=[
		ReferenceBlock(target=header),
		TextBlock(content=dict(en='''<h2>Terms of Use</h2>

<p>PLEASE READ THESE TERMS OF USE ("AGREEMENT" OR "TERMS OF USE") CAREFULLY BEFORE USING THE WEBSITE, MOBILE APPLICATIONS, AND SERVICES OFFERED BY SOMECOMPANY, INC. AND ITS SUBSIDIARIES (COLLECTIVELY, "SOMECOMPANY"). THIS AGREEMENT SETS FORTH THE LEGALLY BINDING TERMS AND CONDITIONS FOR YOUR USE OF THE&nbsp;WEBSITE AT WWW.EXAMPLE.COM (THE "SITE"), MOBILE APPLICATIONS, AND SERVICES PROVIDED BY SOMECOMPANY (COLLECTIVELY, THE “SERVICES”).</p>
<p>By using the Services&nbsp;in any manner, including but not limited to visiting or browsing the Site, you (the "user" or "you") agree to be bound by this Agreement, including those additional terms and conditions and policies referenced herein and/or available by hyperlink. This Agreement applies to all users of the Services, including without limitation users who are vendors, customers, merchants, contributors of content, information and other materials or services on the Site.</p>
<p>If you have any questions, please refer to the <a title="Help" href="http://www.example.com/ca/help" target="_blank">Help</a> section of the Site.</p>
<p><br><br><br><br> <em> Effective Date: October 27, 2009<br>Updated: <em>October 27</em>, 2014<br></em></p>''')),
		ReferenceBlock(target=footer),
	]).save()
root = root.append(terms)

privacy = Page(name='privacy', title=dict(en="Privacy Policy"), content=[
		ReferenceBlock(target=header),
		TextBlock(content=dict(en='''<h2>Privacy Policy</h2>

<p>We love our community at Example Company. You’ve trusted us with a big responsibility, and we’re committed to upholding a high standard when it comes to our privacy practices. It’s important to us that you’re comfortable on our site, so we provide options for you to control how much information you share and your communication preferences. We use secure technologies and follow best practices, as evidenced by TRUSTe's Privacy Seal, recognized and trusted by millions of consumers as a sign of responsible privacy practices. We believe in being transparent about our practices, which is why we provide a detailed <a href="#privacy">Privacy Policy</a> to explain how we gather, use and protect your information. We’ve pulled out the highlights here, in an effort to better communicate the key points.<br><br>By visiting our website or using our mobile applications, you are accepting the terms of this Privacy Policy. Any external links to other websites are clearly identifiable as such, and we are not responsible for the content or the privacy policies of these other websites.&nbsp;</p>
<p>Current policy published: June 09, 2014<br><br></p>''')),
		ReferenceBlock(target=footer),
	]).save()
root = root.append(privacy)

colophon = Page(name='colophon', title=dict(en="Site Colophon"), content = [
		ReferenceBlock(target=header),
		ReferenceBlock(target=footer),
	]).save()
root = root.append(colophon)


# Now that we're done construction, display our glorious sitemap.
root.tree()

from pprint import pprint

print()
pprint(list(Asset.objects.scalar('name', 'path')))
print()
pprint(list(Asset.objects.scalar('parent')))
print()
pprint(list(Asset.objects.scalar('parents').no_dereference()))
print()
root = root.reload()
print()
print()
pprint(root)
print()
pprint(list(root.children))
print()
pprint(list(root.children.named('terms')))
print()
pprint(list(root.children.named('careers')))
