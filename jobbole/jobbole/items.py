# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader
from jobbole.models.es_type import JobboleItemType
from w3lib.html import remove_tags
from elasticsearch_dsl.connections import connections
es = connections.create_connection(JobboleItemType._doc_type.using)


def gen_suggests(index, info_tuple):
    #根据字符串生成搜索建议数组
    used_words = set() #set为去重功能
    suggests = []
    for text, weight in info_tuple:
        if text:
            #字符串不为空时，调用elasticsearch的analyze接口分析字符串（分词、大小写转换）
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter':["lowercase"]}, body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({'input': list(new_words), 'weight': weight})
    return suggests


class MyItemLoader(ItemLoader):
    #默认itemloader返回一个列表,这里重构代码默认返回列表第一个元素
    default_output_processor = TakeFirst()

#处理时间
from datetime import datetime
def format_date(value):
    value = value.replace('·','').strip()
    try:
        date = datetime.strptime(value,"%Y/%m/%d").date()
    except:
        date = datetime.now().date()
    return date
#处理tag
def remove_comment_tag(value):
    if "评论" in value:
        return ""
    else:
        return value
class JobboleItem(scrapy.Item):
    url = scrapy.Field()
    url_obj_id = scrapy.Field()
    title = scrapy.Field()
    create_time = scrapy.Field(
        input_processor=MapCompose(format_date)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tag),
        output_processor=Join(' ')
    )
    content = scrapy.Field()

    def get_sql(self):
        insert_sql = """
            insert into article(title, create_date, url, url_object_id, tags, content)
            values(%s,%s,%s,%s,%s,%s)
        """
        params = (self['title'], self['create_time'],self['url'],self['url_obj_id'],self['tags'],self['content'])
        return insert_sql,params

    def save_es(self):
            # 将item转换为es格式
            data = JobboleItemType()
            data.title = self['title']
            data.create_time = self['create_time']
            # remove_tags去除content中的html标签
            data.content = remove_tags(self['content'])
            data.tags = self['tags']
            data.url = self['url']
            data.meta.id = self['url_obj_id']

            #生成搜索建议词
            data.suggest = gen_suggests(JobboleItemType._doc_type.index, ((data.title, 10), (data.tags, 5)))
            data.save()

            return