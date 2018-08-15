# -*- coding: utf-8 -*-
import scrapy
from movieproject.items import MovieprojectItem

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['www.id97.com']
    start_urls = ['http://www.id97.com/movie/']

    page = 1
    url = 'http://www.id97.com/movie/?page={}'

    def parse(self, response):
        div_list =response.xpath('//div[starts-with(@class,"col-xs-1-5")]')
        for odiv in div_list:
            item = MovieprojectItem()
            item['poster'] = odiv.xpath('.//img/@data-original').extract()[0]
            item['name'] = odiv.xpath('.//h1/a/text()').extract()[0]
            item['score'] = odiv.xpath('.//h1/em/text()').extract()[0]
            item['movie_type'] = odiv.xpath('.//div[@class = "otherinfo"]').xpath('string(.)').extract()[0]
            detail_url = odiv.xpath('.//h1/a/@href').extract()[0]
            yield scrapy.Request(url=detail_url,callback=self.parse_detail,meta={'xxx':item})

        if self.page <= 2:
            self.page += 1
            url = self.url.format(self.page)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_detail(self,response):
        # 提取item
        item = response.meta['xxx']
        item['director'] = response.xpath('//span[contains(text(),"导演")]/../../td[2]')[0].xpath('string(.)').extract()[0]
        try:
            item['editor'] = response.xpath('//span[contains(text(),"编剧")]/../../td[2]')[0].xpath('string(.)').extract()[0]
            item['actor'] = response.xpath('//span[contains(text(),"主演")]/../../td[2]')[0].xpath('string(.)').extract()[0].rstrip(' 显示全部')
        except:
            item['editor'] = ''
            item['actor'] = ''
        item['area'] = response.xpath('//span[contains(text(),"地区")]/../../td[2]')[0].xpath('string(.)').extract()[0]
        item['publish_time'] = response.xpath('//span[contains(text(),"上映时间")]/../../td[2]')[0].xpath('string(.)').extract()[
            0]
        item['info'] = response.xpath('//div[@class="col-xs-12 movie-introduce"]/p/text()')[0].extract().strip('\u3000')
        print(item)
        yield item