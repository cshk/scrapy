from scrapy_redis.spiders import RedisSpider
from zufang.util.InsertToRedis import insert_req,insert_start
import re


class ZfSpider(RedisSpider):
    name = 'zufang'
    redis_key = 'start_urls'


    def parse(self, response):
        response_url = re.findall('^http\:\/\/\w+\.58\.com', response.url)
        next_link = response.xpath('//a[@class="next"]/@href').extract_first()
        detail_link_lst = response.xpath('//div[@class="listBox"]//li/@logr').extract()

        print(next_link)
        print(detail_link_lst)
        if next_link:
            if detail_link_lst:
                print(next_link)
                insert_start(str(next_link), 1)
                print('####[successful] next_link ' + next_link + ' insert redis queue###')

        for detail in detail_link_lst:
            #构造详情页  默认详情页是跳转的
            detail_link = response_url[0] + '/zufang/'+detail.split('_')[3]+'x.shtml'
            if detail_link:
                insert_req(str(detail_link), 2)
                print('####[successful] detail_link ' + detail_link + ' insert redis queue###')

