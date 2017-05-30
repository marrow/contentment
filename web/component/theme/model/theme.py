from marrow.mongo.document import Asset


class Theme(Asset):
	handler = Asset.handler.adapt(default='theme.default')
