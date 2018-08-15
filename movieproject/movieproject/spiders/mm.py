# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from movieproject.items import MovieprojectItem

class MmSpider(CrawlSpider):
    name = 'mm'
    allowed_domains = ['www.id97.com']
    start_urls = ['http://www.id97.com/movie/']
    page_link = LinkExtractor(allow=r'movie/\?page=\d+')

    rules = (
        Rule(page_link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        div_list = response.xpath('//div[starts-with(@class,"col-xs-1-5")]')
        for odiv in div_list:
            item = MovieprojectItem()
            item['poster'] = odiv.xpath('.//img/@data-original').extract()[0]
            item['name'] = odiv.xpath('.//h1/a/text()').extract()[0]
            item['score'] = odiv.xpath('.//h1/em/text()').extract()[0]
            item['movie_type'] = odiv.xpath('.//div[@class = "otherinfo"]').xpath('string(.)').extract()[0]
            yield item


