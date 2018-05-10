# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from xsspider.items import ChaptersItem, BookItem


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #使用mongodb的update更新命令实现去重。
        if isinstance(item, BookItem):
            self.db.books.update({'url': item['novel_Url']}, {'$set': dict(item)}, True)
        if isinstance(item, ChaptersItem):
            self.db.chapters.update({'url': item['chapter_Url']}, {'$set': dict(item)}, True)
        return item


