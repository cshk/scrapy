# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XunyingItem(scrapy.Item):
    name = scrapy.Field()
    #又名
    rname = scrapy.Field()
    screenwriter = scrapy.Field()
    director = scrapy.Field()
    star = scrapy.Field()
    type = scrapy.Field()
    area = scrapy.Field()
    language = scrapy.Field()
    long = scrapy.Field()
    score = scrapy.Field()
    time = scrapy.Field()
    introduce = scrapy.Field()
    tags = scrapy.Field()
    source = scrapy.Field()