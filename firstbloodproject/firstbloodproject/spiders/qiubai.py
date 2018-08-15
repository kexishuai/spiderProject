# -*- coding: utf-8 -*-
# 导入scrapy
import scrapy
from firstbloodproject.items import FirstbloodprojectItem

class QiubaiSpider(scrapy.Spider):
    # 爬虫名称
    name = 'qiubai'
    # 允许的域名,只能爬取该域名下所有url
    allowed_domains = ['www.qiushibaike.com']
    # 起始url,可写多个
    start_urls = ['http://www.qiushibaike.com/']

    page = 1

    url = 'https://www.qiushibaike.com/8hr/page/{}/'
    # 重写函数,名字不能变
    # response:响应对象
    # 函数如果有返回值,要返回一个可迭代对象
    def parse(self, response):
        # print(response.text)
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
            item['age'] =age
            item['content'] = content
            item['haha_count'] = haha_count
            item['ping_count'] = ping_count

            yield item

        if self.page <= 2:
            self.page += 1
            url = self.url.format(self.page)
            yield scrapy.Request(url=url,callback=self.parse)

            # item = {
            #     '头像': face,
            #     '用户名': name,
            #     '年龄': age,
            #     '内容': content,
            #     '好笑个数': haha_count,
            #     '评论个数': ping_count,
            # }
            # print(items)
            # items.append(item)

        # return items
       # print('*'*100)
