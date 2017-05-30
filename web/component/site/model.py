from marrow.mongo.document import Asset


class Site(Asset):
	handler = Asset.handler.adapt(default='site.default')
