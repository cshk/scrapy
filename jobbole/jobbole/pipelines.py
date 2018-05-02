# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
from twisted.enterprise import adbapi

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        #异步操作
        query = self.dbpool.runInteraction(self.data_insert, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        #异步插入异常
        print(failure)

    def data_insert(self, cursor, item):
        #数据插入
        insert_sql , params = item.get_sql()
        cursor.execute(insert_sql,(item['title'], item['create_time'],item['url'],
                                        item['url_obj_id'],item['tags'],item['content']))


class ElasticsearchPipeline(object):
    #数据写入到es
    def process_item(self, item, spider):
        item.save_es()
        return item