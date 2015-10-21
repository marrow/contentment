# encoding: utf-8

from mongoengine import EmbeddedDocument



class ACLRule(EmbeddedDocument):
	meta = dict(allow_inheritance=True)
	
	pass
