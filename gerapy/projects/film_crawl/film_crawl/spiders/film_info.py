# -*- coding: utf-8 -*-
import json
import logging
import scrapy
# from fake_useragent import UserAgent

from ..items import MovieInfoItem


class MovieInfoSpider(scrapy.Spider):
    name = 'film_info'
    allowed_domains = ['api.maoyan.com']

    def __init__(self, film_id=None):
        film_id='247295'
        self.film_id = film_id
        self.start_urls = 'http://api.maoyan.com/mmdb/movie/v5/{}.json'.format(self.film_id)

    def start_requests(self):
        yield scrapy.Request(self.start_urls, callback=self.parse)

    def parse(self, response):
        info = MovieInfoItem()
        try:
            # 将返回数据loads成字典
            items = json.loads(response.text).get('data').get('movie')
            info['movie_id'] = items['id']  # 电影Id
            info['name'] = items['nm']  # 电影名字
            info['enm'] = items['enm']  # 电影英文名
            info['type'] = items['cat']  # 电影类型
            info['region'] = items['src']  # 电影地区
            info['lang'] = items['oriLang']  # 电影语言
            info['score'] = float(items['sc'])  # 电影评分
            info['release_time'] = items['rt']  # 电影上映时间
            # 原url是无效链接，要去到原url中的'/w.h'字符串才是有效链接，并且将Http协议改成https安全协议
            info['img'] = items['img'].replace('http', 'https').replace('/w.h', '')  # 电影海报
            info['videourl'] = items['videourl']  # 电影宣传视频链接
            info['dra'] = items['dra']  # 电影简介
            info['info'] = json.dumps(
                {'movie_id': items['id'], 'name': items['nm'], 'enm': items['enm'], 'type': items['cat'],
                 'region': items['src'], 'lang': items['oriLang'], 'score': float(items['sc']),
                 'release_time': items['rt'], 'img': items['img'].replace('http', 'https').replace('/w.h', ''),
                 'videourl': items['videourl']})
            yield info

        except Exception as e:
            self.logger.error(e)
