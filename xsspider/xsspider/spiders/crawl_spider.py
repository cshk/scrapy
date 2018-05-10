# import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractor import LinkExtractor
# from xsspider.items import BookItem, ChaptersItem
# import re
#
#
# class NovelSpider(CrawlSpider):
#     name = '23us_spider'
#     allowed_domains=["23us.so"]
#     start_urls = ['http://www.23us.so/xiaoshuo/13694.html']
#     rules = (
#         #http://www.23us.so/xiaoshuo/13694.html  小说页面
#         Rule(LinkExtractor(allow=("xiaoshuo/\d*\.html")), callback="parse_book_info", follow=True),
#         #http://www.23us.so/files/article/html/13/13694/index.html #小说所有章节列表
#         Rule(LinkExtractor(allow=("files/article/html/\d*?/\d*?/index.html")),callback="get_chapters", follow=True),
#         #http://www.23us.so/files/article/html/13/13694/6167429.html#每一章内容
#         Rule(LinkExtractor(allow=("files/article/html/\d*?/\d*?/\d*?.html")),callback="parse_chapter_content", follow=True),
#         Rule(LinkExtractor(allow=(".*?")), follow=True)
#     )
#
#     def parse_book_info(self, response):
#         if not response.body:
#             print(response.url + "is already crawled")
#             return
#         novel_Url = response.url
#         novel_Name = response.xpath("//dl[@id='content']//h1/text()").extract_first().split(" ")[0]
#         novel_ImageUrl = response.xpath("//a[@class='hst']/img/@src").extract_first()
#         novel_ID = int(response.url.split("/")[-1].split(".")[0])
#         novel_Type = response.xpath(".//table[@id='at']/tr[1]/td[1]/a/text()").extract_first()
#         novel_Author = response.xpath(".//table[@id='at']/tr[1]/td[2]/text()").extract_first().strip()
#         novel_Status = response.xpath(".//table[@id='at']/tr[1]/td[3]/text()").extract_first().strip()
#         novel_Collect = response.xpath(".//table[@id='at']/tr[2]/td[1]/text()").extract_first().strip()
#         novel_Words = response.xpath(".//table[@id='at']/tr[2]/td[2]/text()").extract_first().strip()
#         novel_UpdateTime = response.xpath(".//table[@id='at']/tr[2]/td[3]/text()").extract_first().strip()
#         novel_Allclick = response.xpath(".//table[@id='at']/tr[3]/td[1]/text()").extract_first().strip()
#         novel_Monclick = response.xpath(".//table[@id='at']/tr[3]/td[2]/text()").extract_first().strip()
#         novel_Weekclick = response.xpath(".//table[@id='at']/tr[3]/td[3]/text()").extract_first().strip()
#         novel_Allcomm = response.xpath(".//table[@id='at']/tr[4]/td[1]/text()").extract_first().strip()
#         novel_Moncomm = response.xpath(".//table[@id='at']/tr[4]/td[2]/text()").extract_first().strip()
#         novel_Weekcomm = response.xpath(".//table[@id='at']/tr[4]/td[3]/text()").extract_first().strip()
#         pattern = re.compile(r'<p>(.*?)<br')
#         novel_Introduction = re.findall(pattern, response.text)[0]
#         bookitem = BookItem(
#             _id= novel_ID,
#             novel_Name = novel_Name,
#             novel_Author = novel_Author,
#             novel_Type = novel_Type,
#             novel_Status = novel_Status,
#             novel_UpdateTime  = novel_UpdateTime,
#             novel_Collect = novel_Collect,
#             novel_Words = novel_Words,
#             novel_ImageUrl = novel_ImageUrl,
#             novel_AllClick = novel_Allclick,
#             novel_MonthClick = novel_Monclick,
#             novel_WeekClick = novel_Weekclick,
#             novel_AllComm = novel_Allcomm,
#             novel_MonthComm = novel_Moncomm,
#             novel_WeekComm = novel_Weekcomm,
#             novel_Url = novel_Url,
#             novel_Introduction = novel_Introduction
#         )
#         return bookitem
#
#
#     def get_chapters(self, response):
#         num = 0
#         all = response.xpath('//tr')
#         for tr in all:
#             td = td.xpaht('.//td[@class="L"]')
#             for url in td:
#                 num += 1
#                 chapter_url = response.url + url.xpath('.//a/@href').extract_first()
#                 chapter_name = url.xpath('.//a/text()').extract_first()
#
#     def parse_chapter_content(self, response):
#         if not response.body:
#             print(response.url + "is already crawled")
#             return
#         novel_Name = response.xpath('//div[@class="bdsub"]/dl/dt/a[3]/text()').extract_first()
#         novel_ID = response.url.split("/")[-2]
#         chapter_Name = response.xpath('.//h1[1]/text()').extract_first()
#         content = response.xpath('//dd[@id="contents"]/text()').extract()
#         chapter_Content = ''.join(x).strip().replace('\xa0', '')
#
#         return ChaptersItem(
#             chapter_Url = response.url,
#             _id = int(response.url.split("/")[-1].split(".")[0]),
#             novel_Name = novel_Name,
#             chapter_Name = chapter_Name,
#             chapter_Content = chapter_Content,
#             novel_ID = novel_ID,
#         )

import scrapy
from xsspider.items import BookItem, ChaptersItem

class DdSpider(scrapy.Spider):
    name = 'dingdian'
    allowed_domains = ['23us.so']
    start_urls=[
        'http://www.23us.so/list/1_1.html',
        'http://www.23us.so/list/2_1.html',
        'http://www.23us.so/list/3_1.html',
        'http://www.23us.so/list/4_1.html',
        'http://www.23us.so/list/5_1.html',
        'http://www.23us.so/list/6_1.html',
        'http://www.23us.so/list/7_1.html',
        'http://www.23us.so/list/8_1.html',
        'http://www.23us.so/list/9_1.html',
    ]

    def parse(self, response):
        #解析所有小说的url信息
        item = BookItem()
        books = response.xpath('//dd/table/tr[@bgcolor="#FFFFFF"]')
        for book in books:
            name = book.xpath('.//td[1]/a[1]/text()').extract_first()
            url = book.xpath('.//td[2]/a[1]/@href').extract_first()
            name_id = url.split('/')[-2]
            author = book.xpath('//td[3]/text()').extract_first()
            words = book.xpath('//td[4]/text()').extract_first()
            uptime = book.xpath('//td[5]/text()').extract_first()
            status = book.xpath('//td[6]/text()').extract_first()
            type = response.xpath('//dl[@id="content"]/dt/text()').extract()[0][:4]

            item['novel_Name'] = name
            item['novel_Author'] = author
            item['novel_Type'] = type
            item['novel_Status'] = status
            item['novel_UpdateTime'] = uptime
            item['novel_Words'] = words
            item['novel_Url'] = url
            item['novel_Id'] = name_id
            yield item
            yield scrapy.Request(url=url, callback=self.get_chapters, meta={'novel_Id':item['novel_Id']})
        next_page = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page)


    def get_chapters(self, response):
        #解析章节的链接
        all_info = response.xpath('//td[@class="L"]')
        for info in all_info:
            chapter_url = info.xpath('./a/@href').extract_first()
            chapter_name = info.xpath('./a/text()').extract_first()
            yield scrapy.Request(chapter_url, callback=self.get_content,
                                 meta = {'novel_Id':response.meta['novel_Id'],
                                         'chapter_name':chapter_name,
                                         'chapter_url':chapter_url})

    def get_content(self, response):
        #解析每一章内容
        item = ChaptersItem()
        item['chapter_ID'] = response.meta['novel_Id']
        item['chapter_Url'] = response.meta['chapter_url']
        item['chapter_Name'] = response.meta['chapter_name']
        content = response.xpath('//dd[@id="contents"]/text()').extract()
        item['chapter_Content'] = ''.join(content).replace('\xa0','').replace('\n','')
        return item


































