# -*- coding: utf-8 -*-

import logging
import pymongo
import pymysql
from scrapy.exceptions import DropItem

from .items import MovieInfoItem, MovieCommentsItem


class TextPipeline(object):
    def __init__(self):
        self.limit = 200

    def process_item(self, item, spider):
        if isinstance(item, MovieInfoItem):
            if len(item['dra']) > self.limit:
                item['dra'] = item['dra'][0:self.limit].rstrip() + '...'
            return item


# 数据清洗，将源数据gender的表示方法统一规范化
class GenderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, MovieCommentsItem):
            if item['gender'] == '1':
                item['gender'] = 'male'
            if item['gender'] == '2':
                item['gender'] = 'female'
            elif item['gender'] == '0':
                item['gender'] = 'unknown'
        return item


class CityPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, MovieCommentsItem):
            if item['cityName'] != 'unknown':
                item['cityName'] = item['cityName'] + '市'
        return item


class MysqlPipeline(object):
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
        try:
            data = dict(item)
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
        except Exception as e:
            logging.error(e)

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









