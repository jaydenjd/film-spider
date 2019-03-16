# -*- coding: utf-8 -*-
import json
import logging
import scrapy
from fake_useragent import UserAgent

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
            items = json.loads(response.text).get('data').get('movie')
            info['movie_id'] = items['id']
            info['name'] = items['nm']
            info['enm'] = items['enm']
            info['type'] = items['cat']
            info['region'] = items['src']
            info['lang'] = items['oriLang']
            info['score'] = float(items['sc'])
            info['release_time'] = items['rt']
            info['img'] = items['img'].replace('http', 'https').replace('/w.h', '')
            info['videourl'] = items['videourl']
            info['dra'] = items['dra']
            info['info'] = json.dumps(
                {'movie_id': items['id'], 'name': items['nm'], 'enm': items['enm'], 'type': items['cat'],
                 'region': items['src'], 'lang': items['oriLang'], 'score': float(items['sc']),
                 'release_time': items['rt'], 'img': items['img'].replace('http', 'https').replace('/w.h', ''),
                 'videourl': items['videourl']})
            yield info

        except Exception as e:
            self.logger.error(e)
