import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dytt.items import DyttItem
import os
import re


class DYTTSpider(CrawlSpider):
    name = 'dytt8.net'
    allowed_domains = ['ygdy8.net', 'dytt8.net']
    start_urls = [
        'http://www.ygdy8.net/html/gndy/rihan/index.html',
        'http://www.ygdy8.net/html/gndy/oumei/index.html',
        'http://www.ygdy8.net/html/gndy/china/index.html',
        'http://www.ygdy8.net/html/gndy/dyzz/index.html',
        'http://www.ygdy8.net/html/gndy/jddy/index.html',
        'http://www.dytt8.net/html/tv/hytv/index.html',
        'http://www.dytt8.net/html/tv/rihantv/index.html',
        'http://www.dytt8.net/html/tv/oumeitv/index.html',
        'http://www.dytt8.net/html/tv/gangtai/index.html',
        'http://www.dytt8.net/html/tv/hepai/index.html',
        'http://www.dytt8.net/html/zongyi2013/index.html',
        'http://www.dytt8.net/html/2009zongyi/index.html',
        'http://www.dytt8.net/html/dongman/index.html'
    ]
    #新建一个文本存储url和时间用来去重
    def __init__(self, *args, **kwargs):
        super(DYTTSpider, self).__init__(*args, **kwargs)
        self.urlset = set()
        if os.path.exists('urlset.txt'):
            with open('urlset.txt', 'r') as fp:
                for line in fp.readlines():
                    if len(line) > 0:
                        self.urlset.add(line)
        else:
            open('urlset.txt', 'w')

    rules = (
        #解析movie
        Rule(LinkExtractor(allow=r'/html/gndy/rihan/list_\d+_\d+.html'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'/html/gndy/oumei/list_\d+_\d+.html'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'/html/gndy/china/list_\d+_\d+.html'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'/html/gndy/dyzz/list_\d+_\d+.html'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'/html/gndy/jddy/list_\d+_\d+.html'), callback='parse_list', follow=True),
        # 解析电视剧
        Rule(LinkExtractor(allow=r'/html/tv/hytv/list_\d+_\d+.html'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'/html/tv/rihantv/list_\d+_\d+.html'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'/html/tv/oumeitv/list_\d+_\d+.html'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'/html/tv/gangtai/list_\d+_\d+.html'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'/html/tv/hepai/list_\d+_\d+.html'), callback='parse_list', follow=True),
        # 解析综艺
        Rule(LinkExtractor(allow=r'/html/zongyi2013/list_\d+_\d+.html'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'/html/2009zongyi/list_\d+_\d+.html'), callback='parse_list', follow=True),
        # 解析动漫
        Rule(LinkExtractor(allow=r'/html/dongman/list_\d+_\d+.html'), callback='parse_list', follow=True),
    )
    def parse_list(self, response):
        url_date = ''
        movies = response.css(".tbspan")

        for movie in movies:
            """
                处理电影url，a标签有两个判断取值
                电影名也一样
            """
            m_movieurl = movie.css('a[class="ulink"]::attr(href)').extract()
            if len(m_movieurl) > 1:
                m_movieurl = m_movieurl[1]
            else:
                m_movieurl = m_movieurl[0]
            m_movieurl = response.urljoin(url=m_movieurl)
            title = movie.css('a[class="ulink"]::text').extract() # 抽取电影标题
            if len(title)>1:
                title = title[1]
            else:
                title = title[0]
            m_title = title
            m_remarks = ''
            m_name = title[title.index(u"《") + 1:title.index(u"》")]  # 电影名称
            m_remarks = title[title.index(u"》") + 1:]  # 电影备注
            date = movie.css('tr>td>font::text').extract_first()
            #从日期和点击之间抽取更新时间
            date = date[date.index("日期")+3:date.index("点击")].strip()
            flag = (m_movieurl+date)
            if flag in self.urlset:
                continue
            else:
                print(flag)
                self.urlset.add(flag)
                url_date += flag
                request = scrapy.Request(url=m_movieurl, callback=self.parse_body)
                request.meta['m_movieurl'] = m_movieurl
                request.meta['m_title'] = m_title
                request.meta['m_name'] = m_name
                request.meta['m_remarks'] = m_remarks
                yield request

        if len(url_date) > 0:
            with open(r'urlset.txt', 'a') as f:
                f.write(url_date)
                url_date = ''

    def parse_body(self, response):
        if 'gndy' in response.url:
            return self.parse_movie(response)
        elif 'tv' in response.url:
            return self.parse_tv(response)
        elif 'zongyi' in response.url:
            return self.parse_zongyi(response)
        elif 'dongman' in response.url:
            return self.parse_dongman(response)
        else:
            return self.parse_movie(response)

    # def parse_movie(self, response):
    #     #电影内容
    #     item = DyttItem()
    #     m_movieurl = response.meta['m_movieurl']
    #     m_name = response.meta['m_name']
    #     m_remarks = response.meta['m_remarks']
    #     m_title = response.meta['m_title']
    # 
    #     content = response.xpath(".//*[@id='Zoom']")
    #     #string(.)返回当前节点所有文本
    #     content = content[0].xpath("string(.)").extract()[0].strip().replace(r'\n', '')
    #     try:
    #         pattern = re.compile(u"◎译[\s\S]*?名([\s\S]*?)◎")
    #         res = re.search(pattern, content)
    #         m_subname = res.groups()[0].strip() #副标题
    #     except BaseException as e:
    #         m_subname = ''
    # 
    #     try:
    #         pattern = re.compile(u"◎类[\s\S]*?别([\s\S]*?)◎")
    #         result = re.search(pattern, content)
    #         m_type = result.groups()[0].strip()#
    #     except Exception as e:
    #         m_type=''
    # 
    #     try:
    #         pattern = re.compile(u"◎产[\s\S]*?地([\s\S]*?)◎")
    #         result = re.search(pattern, content)
    #         m_area = result.groups()[0].strip()  #
    #     except Exception as e:
    #         m_area = ''
    # 
    # 
    # 
    #     try:
    #         pattern = re.compile(u"◎语[\s\S]*?言([\s\S]*?)◎")
    #         result = re.search(pattern, content)
    #         m_lang = result.groups()[0].strip()#
    #     except Exception as e:
    #         m_lang=''
    # 
    #     try:
    #         pattern = re.compile(u"◎年[\s\S]*?代([\s\S]*?)◎")
    #         result = re.search(pattern, content)
    #         m_year = result.groups()[0].strip()#年代
    #     except Exception as e:
    #         m_year=0
    # 
    #     try:
    #         pattern = re.compile(u"◎主[\s\S]*?演([\s\S]*?)◎")
    #         result = re.search(pattern, content)
    #         m_starring = result.groups()[0].strip()#
    #     except Exception as e:
    #         try:
    #             pattern = re.compile(u"◎演[\s\S]*?员([\s\S]*?)◎")
    #             result = re.search(pattern, content)
    #             m_starring = result.groups()[0].strip()#
    #         except Exception as e1:
    #             m_starring = ''
    # 
    # 
    #     try:
    #         pattern = re.compile(u"◎导[\s\S]*?演([\s\S]*?)◎")
    #         result = re.search(pattern, content)
    #         m_directed = result.groups()[0].strip()#
    #     except Exception as e:
    #         m_directed=''
    # 
    #     try:
    #         pattern = re.compile(u"◎片[\s\S]*?长([\s\S]*?)◎")
    #         result = re.search(pattern, content)
    #         m_duration = result.groups()[0].strip()#
    #     except Exception as e:
    #         m_duration=0
    # 
    #     try:
    #         pattern = re.compile(u"◎简[\s\S]*?介([\s\S]*?)【下载地址】")
    #         result = re.search(pattern, content)
    #         m_content = result.groups()[0].strip()#
    #     except Exception as e:
    #         m_content=''
    # 
    #     pic_list = response.css('#Zoom img::attr(src)').extract()
    #     if len(pic_list) > 1:
    #         m_pic = pic_list[0]
    #         m_contentpic = pic_list[1]
    #     elif len(pic_list) == 1:
    #         m_pic = pic_list[0]
    #         m_contentpic = ''
    #     else:
    #         m_pic = ''
    #         m_contentpic = ''
    #     print(
    #         'url:{} name:{} remarks: {} subname: {} type:{} area:{} lang:{} starring:{} directed:{} duration:{} content:{} pic:{} contentpic:{} downurl:{} year:{}'.format(
    #             m_movieurl,m_name,m_remarks,m_subname,type,m_area,m_lang,m_starring,m_directed,m_duration,content,m_pic,m_contentpic,m_downurl,m_year)
    #         )
    # 
    # 
    #     m_downurl = response.css('#Zoom a[href^=ftp]::attr(href)').extract()
    #     item['m_movieurl']=m_movieurl
    #     item['m_name'] = m_name
    #     item['m_remarks'] = m_remarks
    #     item['m_subname'] = m_subname
    #     item['m_type'] = m_type
    #     item['m_area'] = m_area
    #     item['m_lang'] = m_lang
    #     item['m_starring'] = m_starring
    #     item['m_directed'] = m_directed
    #     item['m_duration'] = m_duration
    #     item['m_content'] = m_content
    #     item['m_pic'] = m_pic
    #     item['m_contentpic'] = m_contentpic
    #     item['m_downurl'] = m_downurl
    #     item['m_year']=m_year
    #     yield item
    def parse_tv(self,response):
        item = DyttItem()
        m_movieurl = response.meta['m_movieurl']
        m_name = response.meta['m_name']
        m_remarks = response.meta['m_remarks']
        m_title = response.meta['m_title']
        m_subname = m_type= m_area= m_lang = m_starring= m_directed = m_duration = m_content=m_year=''
        #下面解析电影的其他内容

        content = response.xpath(".//*[@id='Zoom']")
        content = content[0].xpath("string(.)").extract()[0].strip().replace(r'\n','')

        for item in [u"◎译[\s\S]*?名([\s\S]*?)◎",u'\[剧[\s\S]*?名\]:([\s\S]*?)\[',u'【译[\s\S]*?名】：([\s\S]*?)【','']:
            if len(item)<1:
                m_subname = m_name
                break
            pattern = re.compile(item)
            result = re.search(pattern, content)
            if result is None:
                continue
            m_subname = result.groups()
            if len(m_subname)>0:
                m_subname = m_subname[0].strip()
                break


        for item in [u"◎类[\s\S]*?别([\s\S]*?)◎",u'\[类[\s\S]*?型\]:([\s\S]*?)\[',u'【类[\s\S]*?别】：([\s\S]*?)【','']:
            if len(item)<1:
                m_type = ''
                break
            pattern = re.compile(item)
            result = re.search(pattern, content)
            if result is None:
                continue
            m_type = result.groups()
            if len(m_type)>0:
                m_type = m_type[0].strip()
                break


        for item in [u"◎产[\s\S]*?地([\s\S]*?)◎",u"◎国[\s\S]*?家([\s\S]*?)◎",u"◎地[\s\S]*?区([\s\S]*?)◎",u'【国[\s\S]*?家】：([\s\S]*?)【','']:
            if len(item)<1:
                m_area = ''
                break
            pattern = re.compile(item)
            result = re.search(pattern, content)
            if result is None:
                continue
            m_area = result.groups()
            print(m_area)
            print(type(m_area))
            if len(m_area)>0:
                m_area = m_area[0].strip()
                break

        for item in [u"◎语[\s\S]*?言([\s\S]*?)◎",u'【语[\s\S]*?言】：([\s\S]*?)【','']:
            if len(item)<1:
                if u'国语' in m_title:
                    m_lang = u'国语'
                elif u"韩语" in m_title:
                    m_lang = u'韩语'
                elif u'日语' in m_title:
                    m_lang = u'日语'
                elif u'中英' in m_title:
                    m_lang = u'英语'
                else:
                    m_lang = ''
                break
            pattern = re.compile(item)
            result = re.search(pattern, content)
            if result is None:
                continue
            m_lang = result.groups()
            if len(m_lang)>0:
                m_lang = m_lang[0].strip()
                break

        if len(m_area)<1:
            if u'台湾'in m_title:
                m_area = u'台湾'
            elif u"香港" in m_title:
                m_area = u'香港'
            elif u'美剧' in m_title:
                m_area = u'美国'
            elif u"韩语" in m_title:
                m_area = u'韩国'
            elif u'日语' in m_title:
                m_area = u'日本'
            elif u"国语" in m_title:
                m_area = u'大陆'
            else:
                m_area = ''



        for item in [u'【首[\s\S]*?播】：([\s\S]*?)【',u'\[首[\s\S]*?播\]:[\s\S]*?(\d+)[\s\S]*?\[',u"◎年[\s\S]*?代([\s\S]*?)◎",u'[\s\S] * ?(\d +)[\s\S] * ?','']:
            if len(item)<1:
                m_year = 0
                break
            pattern = re.compile(item)
            result = re.search(pattern, content)
            if result is None:
                continue
            m_year = result.groups()
            if len(m_year)>0:
                m_year = m_year[0].strip()
                break



        for item in [u"◎主[\s\S]*?演([\s\S]*?)◎",u"◎演[\s\S]*?员([\s\S]*?)◎",u'【演[\s\S]*?员】：([\s\S]*?)【',u'\[演[\s\S]*?员\]:([\s\S]*?)\[','']:
            if len(item)<1:
                m_starring = ''
                break
            pattern = re.compile(item)
            result = re.search(pattern, content)
            if result is None:
                continue
            m_starring = result.groups()
            if len(m_starring)>0:
                m_starring = m_starring[0].strip()
                break

        for item in [u'【导[\s\S]*?演】：([\s\S]*?)【',u"◎导[\s\S]*?演([\s\S]*?)◎",u'\[导[\s\S]*?演\]:([\s\S]*?)\[','']:
            if len(item)<1:
                m_directed = ''
                break
            pattern = re.compile(item)
            result = re.search(pattern, content)
            if result is None:
                continue
            m_directed = result.groups()
            if len(m_directed)>0:
                m_directed = m_directed[0].strip()
                break

        for item in [u'【片[\s\S]*?长】：[\s\S]*?(\d+)[\s\S]*?【',u"◎片[\s\S]*?长([\s\S]*?)◎",'']:
            if len(item)<1:
                m_duration = 0
                break
            pattern = re.compile(item)
            result = re.search(pattern, content)
            if result is None:
                continue
            m_duration = result.groups()
            if len(m_duration)>0:
                m_duration = m_duration[0].strip()
                break

        for item in [u"【简[\s\S]*?介】：([\s\S]*?)【下载地址】",u"◎简[\s\S]*?介([\s\S]*?)【下载地址】",u'\[简[\s\S]*?介\]:([\s\S]*?)【','']:
            if len(item)<1:
                m_content = ''
                break
            pattern = re.compile(item)
            result = re.search(pattern, content)
            if result is None:
                continue
            m_content = result.groups()
            if len(m_content)>0:
                m_content = m_content[0].strip()
                break


        #解析图片链接
        pic_list = response.css("#Zoom img::attr(src)").extract()
        if len(pic_list)>1 :
            m_pic = pic_list[0]
            m_contentpic = pic_list[1]
        elif len(pic_list)==1:
            m_pic = pic_list[0]
            m_contentpic=''
        else:
            m_pic = ''
            m_contentpic=''

        m_downurl = response.css("#Zoom a[href^=ftp]::attr(href)").extract()
        item['m_movieurl']=m_movieurl
        item['m_name'] = m_name
        item['m_remarks'] = m_remarks
        item['m_subname'] = m_subname
        item['m_type'] = m_type
        item['m_area'] = m_area
        item['m_lang'] = m_lang
        item['m_starring'] = m_starring
        item['m_directed'] = m_directed
        item['m_duration'] = m_duration
        item['m_content'] = m_content
        item['m_pic'] = m_pic
        item['m_contentpic'] = m_contentpic
        item['m_downurl'] = m_downurl
        item['m_year']=m_year
        print(item[0])
        yield item

    def parse_zongyi(self, response):
        item = DyttItem()
        m_movieUrl = response.meta['m_movieUrl']
        m_name = response.meta['m_name']
        m_remarks = response.meta['m_remarks']
        m_title = response.meta['m_title']

        # 下面解析电影的其他内容
        ##Zoom>span>img提取图片

        content = response.xpath(".//*[@id='Zoom']")
        content = content[0].xpath("string(.)").extract()[0].strip().replace(r'\n', '')
        m_subname = ''

        pattern = re.compile(u'\[([\s\S]*?)\][\s\S]*?(\d{4})[\s\S]*?')
        result = re.search(pattern, m_title)
        m_type = ''
        m_year = 0
        if result is not None:
            m_type = result.groups()
            if m_type > 1:
                m_type = m_type[0].strip()
                m_year = m_type[1].strip()
        if u"台湾综艺" in m_type or u"香港综艺" in m_type:
            m_type = u"港台综艺"

        m_area = ''
        m_lang = ''

        m_starring = ''
        m_directed = ''
        m_duration = 0
        m_content = content

        # 解析图片链接
        pic_list = response.css("#Zoom img::attr(src)").extract()
        if len(pic_list) > 1:
            m_pic = pic_list[0]
            m_contentpic = pic_list[1]
        elif len(pic_list) == 1:
            m_pic = pic_list[0]
            m_contentpic = ''
        else:
            m_pic = ''
            m_contentpic = ''

        m_downurl = response.css("#Zoom a[href^=ftp]::attr(href)").extract()
        m_class = ''
        item['m_movieUrl'] = m_movieUrl
        item['m_name'] = m_name
        item['m_remarks'] = m_remarks
        item['m_subname'] = m_subname
        item['m_type'] = m_type
        item['m_area'] = m_area
        item['m_lang'] = m_lang
        item['m_starring'] = m_starring
        item['m_directed'] = m_directed
        item['m_duration'] = m_duration
        item['m_content'] = m_content
        item['m_pic'] = m_pic
        item['m_contentpic'] = m_contentpic
        item['m_downurl'] = m_downurl
        item['m_year'] = m_year
        yield item

    def parse_dongman(self, response):
        item = DyttItem()
        m_movieUrl = response.meta['m_movieUrl']
        m_name = response.meta['m_name']
        m_remarks = response.meta['m_remarks']
        m_title = response.meta['m_title']

        # 下面解析电影的其他内容
        ##Zoom>span>img提取图片

        content = response.xpath(".//*[@id='Zoom']")
        content = content[0].xpath("string(.)").extract()[0].strip().replace(r'\n', '')
        m_subname = ''

        pattern = re.compile(u'\[([\s\S]*?)\]([\s\S]*)')
        result = re.search(pattern, m_title)
        m_type = ''
        m_year = 0
        if result is not None:
            m_type = result.groups()
            if m_type > 1:
                m_type = m_type[0].strip()

        m_area = ''
        m_lang = ''

        m_starring = ''
        m_directed = ''
        m_duration = 0
        m_content = content

        # 解析图片链接
        pic_list = response.css("#Zoom img::attr(src)").extract()
        if len(pic_list) > 1:
            m_pic = pic_list[0]
            m_contentpic = pic_list[1]
        elif len(pic_list) == 1:
            m_pic = pic_list[0]
            m_contentpic = ''
        else:
            m_pic = ''
            m_contentpic = ''

        m_downurl = response.css("#Zoom a[href^=ftp]::attr(href)").extract()
        m_class = ''
        item['m_movieUrl'] = m_movieUrl
        item['m_name'] = m_name
        item['m_remarks'] = m_remarks
        item['m_subname'] = m_subname
        item['m_type'] = m_type
        item['m_area'] = m_area
        item['m_lang'] = m_lang
        item['m_starring'] = m_starring
        item['m_directed'] = m_directed
        item['m_duration'] = m_duration
        item['m_content'] = m_content
        item['m_pic'] = m_pic
        item['m_contentpic'] = m_contentpic
        item['m_downurl'] = m_downurl
        item['m_year'] = m_year
        item['m_class'] = m_class
        yield item