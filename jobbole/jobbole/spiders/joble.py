# -*- coding: utf-8 -*-
import scrapy
from jobbole.items import MyItemLoader, JobboleItem
from jobbole.utils.comment import get_md5
from scrapy_redis.spiders import RedisSpider

class JobleSpider(RedisSpider):
    name = 'joble'
    allowed_domains = ['blog.jobbole.com']
    redis_key = 'joble:start_urls'
    def parse(self, response):
        #获取当前页面的所有文章url,然后进行内容解析
        urls = response.css('#archive .floated-thumb .post-thumb a::attr(href)').extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)

        #下一页
        next_urls = response.xpath('//a[@class="page-numbers"]/@href').extract_first()
        if next_urls:
            yield scrapy.Request(url=next_urls, callback=self.parse)
    def parse_detail(self, response):
        # item = JobboleItem()
        # title = response.xpath("//div[@class='entry-header']/h1/text()").extract_first()
        # create_time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().strip().replace('·','')
        # content = response.xpath('//div[@class="entry"]').extract_first()
        # tag_lst = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tag_lst = [element for element in tag_lst]
        # tags = ",".join(tag_lst)
        #
        # item['url_obj_id'] = get_md5(response.url)
        # item['url'] = response.url
        # item['title'] = title
        # item['create_time'] = create_time
        # item['tags'] = tags
        # item['content'] = content

        item_loader = MyItemLoader(item=JobboleItem(), response=response)
        item_loader.add_xpath("title", "//div[@class='entry-header']/h1/text()")
        item_loader.add_xpath("create_time", '//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_obj_id", get_md5(response.url))
        item_loader.add_xpath("tags", '//p[@class="entry-meta-hide-on-mobile"]/a/text()')
        item_loader.add_xpath("content", '//div[@class="entry"]')
        item = item_loader.load_item()
        yield item
