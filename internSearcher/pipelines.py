# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from datetime import datetime
from internSearcher.items import Vacancy

import logging
logger = logging.getLogger('*Pipeline Logger*')


class InternsearcherPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoStoragePipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        possibleDuplicate = None
        if isinstance(item, Vacancy):
            possibleDuplicate = self.db[item['collections']].find_one({
                'title': item['title'],
                'employer': item['employer'],
                'jd': item['jd']
            })
            if possibleDuplicate:
                self.db[item['collections']].update_one({
                    '_id': possibleDuplicate['_id']
            }, {
                '$set': {**dict(possibleDuplicate), **{'lastSeenDate': datetime.now()}}
            })
            else:
                self.db[item['collections']].insert_one({**dict(item), **{'lastSeenDate': datetime.now(), 'createdAt': datetime.now()}})
        return item

    def close_spider(self, spider):
        self.client.close()
