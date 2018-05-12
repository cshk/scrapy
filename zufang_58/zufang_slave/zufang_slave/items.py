# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZufangItem(scrapy.Item):
    #名称
    title = scrapy.Field()
    #价格
    price = scrapy.Field()
    #租赁方式
    method = scrapy.Field()
    #区域
    area = scrapy.Field()
    #小区
    community = scrapy.Field()
    #详情url
    detail_url = scrapy.Field()
    #发布时间
    pub_time = scrapy.Field()
    #城市
    city = scrapy.Field()
    #联系方式
    phone = scrapy.Field()
