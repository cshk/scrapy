# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import  Rule
from scrapy_redis.spiders import RedisCrawlSpider
from xunying.items import XunyingItem
import re

class XymoviesSpider(RedisCrawlSpider):
    name = 'xymovies'
    allowed_domains = ['xunyingwang.com']
    redis_key = 'xymovies:start_urls'
    rules = (
        Rule(LinkExtractor(allow='movie\/\?page=\d+'), follow=True),
        Rule(LinkExtractor(allow='movie\/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = XunyingItem()
        item['name'] = name = response.xpath('//div[@class="col-xs-9 movie-info padding-right-5 "]/h1/text()').extract_first()
        info = response.xpath('//table[@class="table table-striped table-condensed table-bordered"]/tbody/tr')
        key = {
            '评分': 'score',
            '编剧': 'screenwriter',
            '主演': 'star',
            '地区': 'area',
            '上映时间': 'time',
            '片长': 'long',
            '类型': 'type',
            '又名': 'rname',
            '导演': 'director',
            '语言': 'language'
        }
        for i in info:
            print(info)
            print(i)
            k = i.xpath('./td[1]/span/text()').extract()[0]
            v = "".join(i.xpath('./td[2]/a/text() | ./td[2]/text()').extract())
            item[key.get(k)] = v.strip().replace('显示全部', "")
        pattern = re.compile('\d+')
        id = pattern.search(response.url).group()
        baseurl = 'http://www.xunyingwang.com/videos/resList/'
        yield scrapy.Request(baseurl+id+"#normalDown", meta={'item':item}, callback=self.GetDownloadUrl)

    def GetDownloadUrl(self, response):
        item = response.meta['item']
        item['source'] = link1 = response.xpath('//*[@rel="nofollow"]/@href').extract()
        yield item




