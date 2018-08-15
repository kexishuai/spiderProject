# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from movieproject.items import MovieprojectItem

class NnSpider(CrawlSpider):
    name = 'nn'
    allowed_domains = ['www.id97.com']
    start_urls = ['http://www.id97.com/movie/']

    page_link = LinkExtractor(allow=r'movie/\?page=\d+')
    detail_link = LinkExtractor(restrict_xpaths='//div[@class="movie-item-in"]/a')

    rules = (
        Rule(page_link,follow=True),
        Rule(detail_link,callback='parse_item',follow=False)
    )

    custom_settings = {
        'ITEM_PIPELINES':{
            'movieproject.pipelines.MovieMysqlPipeline': 301,
        }
    }

    def parse_item(self, response):
        # 提取item
        item = MovieprojectItem()

        item['poster'] = response.xpath('//a[@class="movie-post"]/img/@src').extract_first()

        item['name'] = response.xpath('//h1')[0].xpath('string(.)').extract_first()

        item['movie_type'] = response.xpath('//span[contains(text(),"类型")]/../../td[2]')[0].xpath('string(.)').extract()[0]

        item['score'] = response.xpath('//span[contains(text(),"评分")]/../../td[2]')[0].xpath('string(.)').extract_first()
        item['director'] = response.xpath('//span[contains(text(),"导演")]/../../td[2]')[0].xpath('string(.)').extract()[0]
        try:
            item['editor'] = response.xpath('//span[contains(text(),"编剧")]/../../td[2]')[0].xpath('string(.)').extract()[0]
            item['actor'] = response.xpath('//span[contains(text(),"主演")]/../../td[2]')[0].xpath('string(.)').extract()[0].rstrip(' 显示全部')
        except:
            item['editor'] = ''
            item['actor'] = ''
        item['area'] = response.xpath('//span[contains(text(),"地区")]/../../td[2]')[0].xpath('string(.)').extract()[0]
        item['publish_time'] = response.xpath('//span[contains(text(),"上映时间")]/../../td[2]')[0].xpath('string(.)').extract()[0]
        item['info'] = response.xpath('//div[@class="col-xs-12 movie-introduce"]/p/text()')[0].extract().strip('\u3000')

        yield item