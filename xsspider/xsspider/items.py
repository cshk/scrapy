# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    """
        小说信息
        定义小说id，用来定位章节信息，章节唯一
    """

    novel_Id = scrapy.Field()#小说编号
    novel_Name = scrapy.Field()  # 小说名称
    novel_Author = scrapy.Field()  # 小说作者
    novel_Type = scrapy.Field()  # 小说类型
    novel_Status = scrapy.Field()  # 小说状态，连载或者完结
    novel_UpdateTime = scrapy.Field()  # 最后更新时间
    novel_Words = scrapy.Field()  # 总字数
    novel_Url = scrapy.Field()  # 小说url
class ChaptersItem(scrapy.Item):
    """
        章节信息
    """
    chapter_Url = scrapy.Field()#章节url
    chapter_Name = scrapy.Field()#章节名称
    chapter_Content = scrapy.Field()#内容
    chapter_ID = scrapy.Field()#小说编号




