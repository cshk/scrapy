# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from YunqiCrawl.items import  YunqiListItem
import re

class YunqicrawlPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB', 'yunqi'),
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, YunqiListItem):
            self._process_booklist_item(item)
        else:
            self._process_bookdetail_item(item)
        return item

    def _process_booklist_item(self, item):
        self.db.bookInfo.insert(dict(item))

    def _process_bookdetail_item(self, item):
        #数据清洗，比如这里的总字数，只提取数字
        pattern = re.compile('\d+')
        item['novelLabel'] = item['novelLabel'].replace('\n', '').strip()

        match = pattern.search(item['novelAllClick'])
        item['novelAllClick'] = match.group() if match else item['novelAllClick']

        match = pattern.search(item['novelMonthClick'])
        item['novelMonthClick'] = match.group() if match else item['novelMonthClick']

        match = pattern.search(item['novelWeekClick'])
        item['novelWeekClick'] = match.group() if match else item['novelWeekClick']

        match = pattern.search(item['novelAllPopular'])
        item['novelAllPopular'] = match.group() if match else item['novelAllPopular']

        match = pattern.search(item['novelMonthPopular'])
        item['novelMonthPopular'] = match.group() if match else item['novelMonthPopular']

        match = pattern.search(item['novelWeekPopular'])
        item['novelWeekPopular'] = match.group() if match else item['novelWeekPopular']

        match = pattern.search(item['novelAllRecom'])
        item['novelAllRecom'] = match.group() if match else item['novelAllRecom']

        match = pattern.search(item['novelMonthRecom'])
        item['novelMonthRecom'] = match.group() if match else item['novelMonthRecom']

        match = pattern.search(item['novelWeekRecom'])
        item['novelWeekRecom'] = match.group() if match else item['novelWeekRecom']

        self.db.bookhot.insert(dict(item))


