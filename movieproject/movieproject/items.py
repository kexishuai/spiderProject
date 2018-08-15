# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    poster = scrapy.Field()
    name = scrapy.Field()
    score = scrapy.Field()
    movie_type = scrapy.Field()

    # 第二个页面
    director = scrapy.Field()
    editor = scrapy.Field()
    actor = scrapy.Field()
    area = scrapy.Field()
    publish_time = scrapy.Field()
    info = scrapy.Field()
