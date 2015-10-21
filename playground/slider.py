# encoding: utf-8

from datetime import datetime
from collections import namedtuple
from itertools import chain

from pytz import utc
from bson import ObjectId
from mongoengine import CASCADE
from mongoengine import Document, EmbeddedDocument
from mongoengine import ListField, StringField, IntField, MapField, BooleanField, DateTimeField, ObjectIdField, FileField
from mongoengine import CachedReferenceField, EmbeddedDocumentField, EmbeddedDocument, DynamicEmbeddedDocument
from mongoengine.fields import RECURSIVE_REFERENCE_CONSTANT
from mongoengine.signals import pre_save, pre_save_post_validation, post_save, pre_delete, post_delete



'''


class Slider(NestedBlock):
	pass



class SlideImage(Block):
	path = StringField(db_field='p')
	left = IntField(db_field='l', default=0)
	top = IntField(db_field='t', default=0)
	depth = IntField(db_field='d', defualt=1)
	speed = IntField(db_field='s', default=500)


class Slide(NestedBlock):
	background = StringField(db_field='b')
	content = EmbeddedDocumentField(Content, db_field='C', default=Content)
	contents = ListField(EmbeddedDocumentField(SlideImage), db_field='c', default=list)


if __name__ == '__main__':
	from mongoengine import connect
	connect('cms')
	
	Asset.drop_collection()
	Asset.ensure_indexes()
	
	import pudb
	# pudb.set_trace()
	
	root = Asset(name='/', path='/careers.example.com', title=dict(en="Publicite Illico Hodes", fr="Publicité Illico Hodes"), handler='careers').save()
	
	careers1 = Page(name='careers', title=dict(en="Careers at Illico Hodes")).appendTo(root)
	jobs1 = Employment(name='job', title=dict(en="Job Details")).appendTo(root)
	
	theme1 = Asset(name='theme', title=dict(en="Site Theme")).appendTo(root)
	images1 = Asset(name='img', title=dict(en="Images")).appendTo(theme1)
	styles1 = Asset(name='css', title=dict(en="Styles")).appendTo(theme1)
	scripts1 = Asset(name='js', title=dict(en="Scripts")).appendTo(theme1)
	
	colophon1 = Asset(name='colophon', title=dict(en="Site Colophon")).appendTo(root)
	privacy1 = Asset(name='privacy', title=dict(en="Privacy Policy")).appendTo(root)
	terms1 = Asset(name='terms', title=dict(en="Terms of Service")).appendTo(root)
	
	
	rita = Asset(name='/', path='/rita.illicohodes.com', title=dict(en="RITA - Publicite Illico Hodes", fr="RITA - Publicité Illico Hodes"), handler='default').save()
	
	default = Page(name='defualt', title=dict(en="Welcome")).appendTo(rita)
	webinars = Asset(name='webinar', title=dict(en="Webinars")).appendTo(default)
	testimonials = Asset(name='testimonial', title=dict(en="Testimonials")).appendTo(default)
	about = Page(name='about', title=dict(en="About Us")).appendTo(rita)
	
	features = Page(name='features', title=dict(en="Features")).appendTo(rita)
	sources = Page(name='sources', title=dict(en="Sources")).appendTo(rita)
	services = Page(name='services', title=dict(en="Services")).appendTo(rita)
	blog = Redirect(name='blog', title=dict(en="Blog"), target='http://www.marketing-employeur.ca/').appendTo(rita)
	contact = Page(name='contact', title=dict(en="Contact Us")).appendTo(rita)
	
	careers = Page(name='careers', title=dict(en="Careers at Illico Hodes")).appendTo(rita)
	jobs = Employment(name='job', title=dict(en="Job Details")).appendTo(careers)
	
	theme = Asset(name='theme', title=dict(en="Site Theme")).appendTo(rita)
	images = Asset(name='img', title=dict(en="Images")).appendTo(theme)
	styles = Asset(name='css', title=dict(en="Styles")).appendTo(theme)
	scripts = Asset(name='js', title=dict(en="Scripts")).appendTo(theme)
	
	colophon = Asset(name='colophon', title=dict(en="Site Colophon")).appendTo(rita)
	privacy = Asset(name='privacy', title=dict(en="Privacy Policy")).appendTo(rita)
	terms = Asset(name='terms', title=dict(en="Terms of Service")).appendTo(rita)
	
	
	# Page Content
	
	content = default.content
	
	content.append(Slider(id='feature_slider', contents=[
			Slide(id='showcasing', background='/theme/img/bg/deep-green.jpeg',
				content = Content(content=dict(
						en = "<h2>Your just-in-time recruitment solution.</h2>",
						fr = "<h2>Votre solution de recrutement sur demande.</h2>"
					)),
				contents = [
						SlideImage(path='/theme/img/slide/macbook.jpeg', left=-30, top=120),
					]),
			Slide(id='showcasing', background='/rita.illicohodes.com/theme/img/bg/aqua.jpeg',
				content = Content(content=dict(
						en="<h2>RITA makes job distribution easier than ever.</h2>",
						fr="<h2>RITA rend la diffusion de vos offres d'emploi plus facile que jamais.</h2>"
					)),
				contents = [
						SlideImage(path='/theme/img/slide/left.jpeg', left=-480, top=260),
						SlideImage(path='/theme/img/slide/middle.jpeg', left=-210, top=213, depth=2),
						SlideImage(path='/theme/img/slide/right.jpeg', left=60, top=260),
					]),
			Slide(id='showcasing', background='/rita.illicohodes.com/theme/img/bg/color-splash.jpeg',
				content = Content(content=dict(
						en="""<h2>Rapid distribution, from any device.</h2><a href="/features">Tour the product.</a>""",
						fr="""<h2>À partir de n'importe quel appareil.</h2><a href="/features">Découvrez RITA</a>"""
					)),
				contents = [
						SlideImage(path='/theme/img/slide/ipad.jpeg', left=-472, top=210, depth=3, speed=650),
						SlideImage(path='/theme/img/slide/iphone.jpeg', left=-365, top=270, depth=4),
						SlideImage(path='/theme/img/slide/desktop.jpeg', left=-350, top=135, depth=2, speed=450),
						SlideImage(path='/theme/img/slide/macbook.jpeg', left=-185, top=220, speed=550),
					]),
			Slide(id='showcasing', background='/rita.illicohodes.com/theme/img/bg/indigo.jpeg',
				content = Content(content=dict(
						en = """<h2>Built using modern technologies.</h2><a href="/colophon">See the Colophon</a>""",
						fr = """<h2>Utilise les dernières technologies.</h2><a href="/colophon">Aperçu du Colophon</a>"""
					)),
				contents = [
						SlideImage(path='/theme/img/slide/html5.jpeg', left=-472, top=120, depth=3),
						SlideImage(path='/theme/img/slide/css3.jpeg', left=-190, top=120, depth=2, speed=500),
					]),
		]))
	
	content.append()

'''