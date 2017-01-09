import logging
import logging.config
import pymongo
from web.contentment.taxonomy import Taxonomy

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
			}
	})

cli = pymongo.MongoClient()
db = cli.test
db.assets.drop()
assets = db.assets

assets.insert_one({'name': '/', 'path': '/'})
assets.insert_one({'name': 'company'})
assets.insert_one({'name': 'about'})
assets.insert_one({'name': 'careers'})
assets.insert_one({'name': 'services'})
assets.insert_one({'name': 'rita'})

taxonomy = Taxonomy(collection=assets)

from time import time

start = time()
result = taxonomy.named('/').insert(0, taxonomy.named('company'))
duration = (time() - start) * 1000

print("Unattached:", duration, "ms")
__import__('pprint').pprint(result.children.first())

start = time()
result = taxonomy.named('/').insert(0, taxonomy.named('company'))
duration = (time() - start) * 1000

print("Attached:", duration, "ms")
print("taxonomy.named('/').insert(0, taxonomy.named('company'))")

