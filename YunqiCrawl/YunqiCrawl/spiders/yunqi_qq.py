# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from YunqiCrawl.items import YunqiBookDetailItem, YunqiListItem
from scrapy.http import Request

class YunqiCrawlSpider(CrawlSpider):
    name = 'yunqi_qq'
    allowed_domains = ['yunqi.qq.com']
    start_urls = ['http://yunqi.qq.com/bk/so2/n30p1']
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'
    }
    rules = (
        Rule(LinkExtractor(allow=r'/bk/so2/n30p\d+'), callback='parse_book_list', follow=True),
    )

    def parse_book_list(self, response):
        books = response.xpath(".//div[@class='book']")
        item = YunqiListItem()
        for book in books:
            item['novelImg'] = book.xpath('./a/img/@src').extract_first()
            item['novelId'] = book.xpath('//div[@class="book_info"]/h3/a/@id').extract_first()
            item['novelName'] = book.xpath('//div[@class="book_info"]/h3/a/text()').extract_first()
            item['novelLink'] = book.xpath('//div[@class="book_info"]/h3/a/@href').extract_first()
            infos = book.xpath('./div[@class="book_info"]/dl/dd[@class="w_auth"]')
            if len(infos) > 4:
                item['novelAuthor'] = infos[0].xpath('./a/text()').extract_first()
                item['novelType'] = infos[1].xpath('./a/text()').extract_first()
                item['novelStatus'] = infos[2].xpath('./text()').extract_first()
                item['novelUT'] = infos[3].xpath('./text()').extract_first()
                item['novelWords'] = infos[4].xpath('./text()').extract_first()
        yield item

        request = scrapy.Request(url=item['novelLink'], callback=self.parse_book_detail, dont_filter=True)
        request.meta['novelId'] = item['novelId']
        yield request


    def parse_book_detail(self, response):
        item = YunqiBookDetailItem()
        item['novelId'] = response.meta['novelId']
        item['novelLabel'] = response.xpath('//div[@class="tags"]/text()').extract_first()
        item['novelAllClick'] = response.xpath('.//*[@id="novelInfo"]/table/tr[2]/td[1]/text()').extract_first()
        item['novelAllPopular'] = response.xpath('.//*[@id="novelInfo"]/table/tr[2]/td[2]/text()').extract_first()
        item['novelAllRecom'] = response.xpath('.//*[@id="novelInfo"]/table/tr[2]/td[3]/text()').extract_first()
        item['novelMonthClick'] = response.xpath('.//*[@id="novelInfo"]/table/tr[3]/td[1]/text()').extract_first()
        item['novelMonthPopular'] = response.xpath('.//*[@id="novelInfo"]/table/tr[3]/td[2]/text()').extract_first()
        item['novelMonthRecom'] = response.xpath('.//*[@id="novelInfo"]/table/tr[3]/td[3]/text()').extract_first()
        item['novelWeekClick'] = response.xpath('.//*[@id="novelInfo"]/table/tr[4]/td[1]/text()').extract_first()
        item['novelWeekPopular'] = response.xpath('.//*[@id="novelInfo"]/table/tr[4]/td[2]/text()').extract_first()
        item['novelWeekRecom'] = response.xpath('.//*[@id="novelInfo"]/table/tr[4]/td[3]/text()').extract_first()
        item['novelCommentNum'] = response.xpath('.//*[@id="novelInfo_commentCount"]/text()').extract_first()
        yield item

