
from scrapy_redis.spiders import RedisSpider
from zufang_slave.items import ZufangItem
import re


class DetailSpider(RedisSpider):
    name = 'slave'
    redis_key = '58_zufang:requests'


    def parse(self, response):
        item = ZufangItem()
        response_url = re.findall('^http\:\/\/\w+\.58\.com', response.url)
        title = response.xpath('//div[@class="house-title"]/h1/text()').extract_first()
        if title:
            item['title'] = title
        pub_time = response.xpath('//p[@class="house-update-info c_888 f12"]/text()').extract_first()
        if pub_time:
            item['pub_time'] = pub_time.strip()
        price = response.xpath('//div[@class="house-pay-way f16"]/span/b/text()').extract_first()
        if price:
            item['price'] = price+'元/月'
        method = response.xpath('//div[@class="house-pay-way f16"]/span[2]/text()').extract_first()
        if method:
            item['method'] = method
        area = response.xpath('//ul[@class="f14"]/li[5]/span[2]/a/text()').extract_first()
        if area:
            item['area'] = area
        community = response.xpath('//a[@class="c_333 ah"]/text()').extract_first()
        if community:
            item['community'] = community
        phone = response.xpath('//p[@class="phone-num"]/text()').extract_first()
        if phone:
            item['phone'] = phone
        item['detail_url'] = response.url
        item['city'] = response.url.split('//')[1].split('.')[0]
        yield item
