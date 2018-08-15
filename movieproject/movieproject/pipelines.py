# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql
from scrapy.utils.project import get_project_settings


class MovieprojectPipeline(object):
    def open_spider(self, spider):
        self.fp = open('movie.txt', 'w', encoding='utf8')

    # 处理item方法
    def process_item(self, item, spider):
        d = dict(item)
        string = json.dumps(d, ensure_ascii=False)

        self.fp.write(string + '\n')
        return item

    def close_spider(self, spider):
        self.fp.close()

class MovieMysqlPipeline(object):
    def open_spider(self, spider):
        settings = get_project_settings()
        host = settings['HOST']
        port = settings['PORT']
        dbname = settings['DBNAME']
        user = settings['USER']
        password = settings['PASSWORD']
        charset = settings['CHARSET']
        self.conn = pymysql.connect(host=host,port=port,db=dbname,user=user,password=password,charset=charset)
        self.cursor = self.conn.cursor()
    # 处理item方法
    def process_item(self, item, spider):
        sql = 'insert into movie(poster,name,score,movie_type,director,editor,actor,area,publish_time,info) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (item["poster"],item["name"],item["score"],item["movie_type"],item["director"],item["editor"],item["actor"],item["area"],item["publish_time"],item["info"])

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print('*'*100)
            print(e)
            print('*'*100)
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()