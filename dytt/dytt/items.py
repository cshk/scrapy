# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DyttItem(scrapy.Item):


    m_movieurl = scrapy.Field()
    m_title = scrapy.Field()
    m_name = scrapy.Field()
    m_subname = scrapy.Field()
    m_type = scrapy.Field()
    m_area = scrapy.Field()
    m_lang = scrapy.Field()
    m_remarks = scrapy.Field()
    m_year = scrapy.Field()
    m_starring = scrapy.Field()
    m_directed = scrapy.Field()
    m_duration=scrapy.Field()

    m_pic = scrapy.Field()
    m_content = scrapy.Field()
    m_contentpic = scrapy.Field()
    m_downurl = scrapy.Field()