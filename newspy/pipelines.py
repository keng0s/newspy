# -*- coding: utf-8 -*-
from pymongo import MongoClient
from scrapy.conf import settings
import ssl


class NewspyPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    def __init__(self):
        connection = MongoClient(settings['MONGODB_HOST'],
                                 port=settings['MONGODB_PORT'],
                                 username=settings['MONGODB_USER'],
                                 password=settings['MONGODB_PASS'],
                                 ssl=True,
                                 ssl_cert_reqs=ssl.CERT_NONE)
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if item['text'] is not None:
            self.collection.insert(dict(item))
            print("Item wrote to MongoDB database %s/%s" %
                   (settings['MONGODB_DB'], settings['MONGODB_COLLECTION'])
            )
        return item
