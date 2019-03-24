# -*- coding: utf-8 -*-
import datetime
import json
import logging
import time
import requests
import scrapy
from scrapy import Request
import sys
sys.path.insert(0, '..')

from ..items import RequestInfoItem


class MaoyanHotfilmSpider(scrapy.Spider):
    name = 'maoyan_hotFilm'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    def __init__(self, *args, **kwargs):
        super(MaoyanHotfilmSpider, self).__init__(*args, **kwargs)
        self.movie_url = 'http://api.maoyan.com/mmdb/movie/v5/{}.json'
        # 城市默认设为广州
        self.hot_movie = 'http://api.maoyan.com/mmdb/movie/v4/list/hot.json?ci=20'

    def get_hotMovie(self):
        hot_movie = 'http://api.maoyan.com/mmdb/movie/v4/list/hot.json?ci=20'
        res = requests.get(hot_movie)
        data = json.loads(res.text)
        # 获取所有热门电影id
        movieIds = data.get('data').get('movieIds')
        return movieIds

    def start_requests(self):
        movieIds = self.get_hotMovie()
        for movie in movieIds:
            yield Request(self.movie_url.format(str(movie)), callback=self.parse_movie)

    # 电影基本信息解析，并构建影评请求
    def parse_movie(self, response):
        req = RequestInfoItem()
        # 初始化获得本地时间
        req_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            # 将返回数据loads成字典
            items = json.loads(response.text).get('data').get('movie')
            if req_time > items['rt']:
                req['movie_id'] = items['id']
                req['movie_name'] = items['nm']
                req['request_date'] = datetime.datetime.now()
                req['create_date'] = datetime.datetime.now()
                if '中国' in items['src']:
                    req['region'] = 'china'
                else:
                    req['region'] = 'foreign'
                yield req
        except Exception as e:
            logging.error(e)


