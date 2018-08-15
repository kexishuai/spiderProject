# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from firstbloodproject.items import FirstbloodprojectItem

class QiuSpider(CrawlSpider):
    name = 'qiu'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['http://www.qiushibaike.com/']

    # 页码链接提取
    page_link = LinkExtractor(allow=r'/8hr/page/\d+/')

    rules = (
        Rule(page_link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print('*' * 100)
        div_list = response.xpath('//div[starts-with(@id,"qiushi_tag")]')
        # print(len(div_list))  # 25
        items = []
        for odiv in div_list:
            # 获取用户头像   这个点必须加
            face = odiv.xpath('.//div[@class="author clearfix"]//img/@src').extract_first()
            # 获取用户名字
            name = odiv.xpath('.//h2/text()')[0].extract()
            # 用户年龄
            age = odiv.xpath('.//div[starts-with(@class,"articleGender")]/text()').extract_first()
            # 发表内容
            content = odiv.xpath('.//div[@class="content"]/span[1]')[0].xpath('string(.)')[0].extract().strip('\n\r\t ')
            # 获取好笑个数
            haha_count = odiv.xpath('.//span[@class="stats-vote"]//i/text()')[0].extract()
            # 获取评论个数
            ping_count = odiv.xpath('.//span[@class="stats-comments"]//i/text()')[0].extract()

            item = FirstbloodprojectItem()

            item['face'] = face
            item['name'] = name
            item['age'] = age
            item['content'] = content
            item['haha_count'] = haha_count
            item['ping_count'] = ping_count

            yield item
