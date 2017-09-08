# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from scrapy.conf import settings
import ssl
import logging


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
        if item['url'] is not None and item['text'] is not None:
            try:
                self.collection.update_one({'url': item['url']}, {'$set': dict(item)}, upsert=True)
            except OperationFailure as e:
                logging.log(logging.ERROR, 'Failed to save to MongoDB: ' + e.details)
        return item
