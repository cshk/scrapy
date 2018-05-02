# -*- coding: utf-8 -*-
import scrapy
import json
import hmac
import time
import base64
from hashlib import sha1
from PIL import Image


class ZhihuspdSpider(scrapy.Spider):
    name = 'zhihuspd'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    headers = {
        'Connection':'Keep-alive',
        'Host': 'www.zhihu.com',
        'Origin': 'https://www.zhihu.com',
        'Referer': 'https://www.zhihu.com/signup?next=%2F',
        'User-Agent': user_agent,
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    }
    grant_type = 'password'
    client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    source = 'com.zhihu.web'
    timestamp = str(int(time.time()*1000))


    def get_signature(self, grant_type, client_id, source, timestamp):
        #处理签名
        h = hmac.new(b'd1b964811afb40118a12068ff74a12f4',None, sha1)
        h.update(str.encode(grant_type))
        h.update(str.encode(client_id))
        h.update(str.encode(source))
        h.update(str.encode(timestamp))
        return str(h.hexdigest())

    def parse(self, response):
        print(response.body.decode('utf-8'))

    def start_requests(self):
        yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
                             headers=self.headers, callback=self.if_need_capture)

    def if_need_capture(self, response):
        print(response.text)
        need_capt = json.loads(response.text)['show_captcha']
        print(need_capt)

        if need_capt:
            print('need input code...')
            yield scrapy.Request(
                url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
                headers=self.headers,
                callback=self.capture,
                method = 'PUT',
            )
        else:
            print('no code , login...')
            post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
            post_data = {
                "client_id": self.client_id,
                "username": "18237191500",  # 输入知乎用户名
                "password": "qq123456789.",  # 输入知乎密码
                "grant_type": self.grant_type,
                "source": self.source,
                "timestamp": self.timestamp,
                "signature": self.get_signature(self.grant_type, self.client_id, self.source, self.timestamp),  # 获取签名
                "lang": "en",
                "ref_source": "homepage",
                "captcha": '',
                "utm_source":'',
            }
            yield scrapy.FormRequest(
                url = post_url,
                formdata=post_data,
                headers=self.headers,
                callback=self.check_login,
            )


    def capture(self, response):
        try:
            image = json.loads(response.text)['img_base64']
        except ValueError:
            print('get img_base64 failed')
        else:
            image = image.encode('utf8')
            image_data = base64.b64decode(image)

            with open('./capture.jpg', 'wb') as f:
                f.write(image_data)
                f.close()
        img = Image.open('./capture.jpg')
        img.show()
        post_data = {
            'input_text':input('input code : ')
        }

        yield scrapy.FormRequest(
            url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
            formdata=post_data,
            headers = self.headers,
            callback=self.captcha_login,
        )

    def captcha_login(self, response):
        try:
            cap_res = json.loads(response.text)['success']
            print(cap_res)
        except:
            print('post failed')
        else:
            if cap_res:
                print('post successful')
        post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        post_data = {
            "client_id": self.client_id,
            "username": "18237191500",  # 输入知乎用户名
            "password": "qq123456789.",  # 输入知乎密码
            "grant_type": self.grant_type,
            "source": self.source,
            "timestamp": self.timestamp,
            "signature": self.get_signature(self.grant_type, self.client_id, self.source, self.timestamp),  # 获取签名
            "lang": "en",
            "ref_source": "homepage",
            "captcha": '',
            "utm_source": '',
        }
        yield scrapy.FormRequest(
            url = post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login,
        )

    def check_login(self, response):
            print(response.text)
            yield scrapy.Request('https://www.zhihu.com/inbox', headers=self.headers)

