# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import pymongo as pymongo
import pymysql

from .items import MovieInfoItem, MovieCommentsItem


class MovieInfoPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8mb4',
                                  port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        # print(item[''])
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        # sql = 'insert into {} ({}) values ({})'.format(item.table, keys, values)
        # self.cursor.execute(sql, (data['movie_id'],
        #                           pymysql.escape_string(data['movie_name']),
        #                           pymysql.escape_string(data['movie_type']),
        #                           pymysql.escape_string(data['movie_region']),
        #                           pymysql.escape_string(data['movie_lang']),
        #                           data['movie_score'],
        #                           pymysql.escape_string(data['movie_release_time']),
        #                           pymysql.escape_string(data['movie_videourl']),
        #                           pymysql.escape_string(data['movie_dra']),
        #                           data['movie_info'],
        #                           )
        #                     )
        # self.cursor.execute(sql, tuple((1, 'dianying', 'act', 'us', 'english', 2.9, '2018-12-2', 'http://baidu.com', 'daha')))
        # sql = sql.format(data['movie_id'],data['movie_name'],data['movie_type'],data['movie_region'],data['movie_lang'],data['movie_score'],
        #                  data['movie_release_time'],data['movie_videourl'],str(data['movie_dra']), str(data['movie_info']))
        # self.cursor.execute(sql)
        self.db.commit()

        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[MovieInfoItem.collection].create_index([('movie_id', pymongo.ASCENDING)])
        self.db[MovieCommentsItem.collection].create_index([('comment_id', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, MovieInfoItem):
            self.db[item.collection].update({'movie_id': item.get('movie_id')}, {'$set': item}, True)
        if isinstance(item, MovieCommentsItem):
            self.db[item.collection].update({'comment_id': item.get('comment_id')}, {'$set': item}, True)









