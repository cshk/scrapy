# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo


class MongoDBPipeline(object):

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
        document = {
            'title':item['title'],
            'price':item['price'],
            'method':item['method'],
            'area':item['area'],
            'community':item['community'],
            'detail_url':item['detail_url'],
            'pub_time':item['pub_time'],
            'city':item['city'],
            'phone':item.get('phone','扫码看电话'),
        }
        self.db.detail_info.insert(document)
        print('the {} insert into MongoDB successful'.format(item['detail_url']))
        return item
