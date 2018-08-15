# -*- coding: utf-8 -*-
import scrapy


class PostSpider(scrapy.Spider):
    name = 'post'
    allowed_domains = ['cn.bing.com']
    start_urls = ['http://cn.bing.com/translator/']

    '''
        def start_requests(self):
            for url in start_urls:
                yield scrapy.Request(url, callback=self.parse)
     '''

    def start_requests(self):
        post_url = 'https://cn.bing.com/ttranslationlookup?&IG=D17ABE1944C94CC5974E9392F2B57441&IID=translator.5036.12'
        data = {
            'from':'zh-CHS',
            'to':'en',
            'text':'美女'
        }
        yield scrapy.FormRequest(url=post_url,formdata=data,callback=self.parse)

    def parse(self, response):
        print('*'*100)
        print(response.text)
        print('*'*100)
