# -*- coding: utf-8 -*-
import json
import logging
import time
import datetime
import scrapy
from urllib.parse import quote
from scrapy import Request
from ..items import *

class DoubanmoviehotSpider(scrapy.Spider):
    name = 'doubanMovieHot'
    allowed_domains = ['douban.com']
    # start_urls = ['http://douban.com/']

    def __init__(self, *args, **kwargs):
        super(DoubanmoviehotSpider, self).__init__(*args, **kwargs)
        self.movie_url = 'http://api.maoyan.com/mmdb/movie/v5/{}.json'
        keyword = '广州'
        # 城市默认设为广州
        self.hot_movie = 'https://api.douban.com/v2/movie/in_theaters?city={}&start=0&count=100'.format(quote(keyword))

    def start_requests(self):
        yield Request(self.hot_movie, callback=self.parse_movie)

    def parse_movie(self, response):
        req = DoubanRequestItem()
        # 初始化获得本地时间
        # req_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            # 将返回数据loads成字典
            subjects = json.loads(response.text).get('subjects')
            for items in subjects:
            # if req_time > items['rt']:
                req['movie_id'] = items['id']
                req['movie_name'] = items['title']
                req['request_date'] = datetime.datetime.now()
                req['create_date'] = datetime.datetime.now()
                req['region'] = 'china'
            # if '中国' in items['src']:
            #     req['region'] = 'china'
            # else:
            #     req['region'] = 'foreign'
                yield req
        except Exception as e:
            logging.error(e)
