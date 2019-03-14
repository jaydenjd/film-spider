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
        self.film_id = film_id
        # self.film_id = '410629'
        self.start_urls = 'http://api.maoyan.com/mmdb/movie/v5/{}.json'.format(self.film_id)

    def start_requests(self):
        ua: UserAgent()
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 "
                          "Safari/537.36"
        }
        yield scrapy.Request(self.start_urls, callback=self.parse, headers=headers)

    def parse(self, response):
        info = MovieInfoItem()
        try:
            items = json.loads(response.text).get('data').get('movie')
            info['movie_id'] = items['id']
            info['movie_name'] = items['nm']
            info['movie_type'] = items['cat']
            info['movie_region'] = items['src']
            info['movie_lang'] = items['oriLang']
            info['movie_score'] = float(items['sc'])
            info['movie_release_time'] = items['rt']
            info['movie_videourl'] = items['videourl']
            info['movie_dra'] = items['dra']
            # info['movie_info'] = json.dumps({
            #     'movie_id': items['id'],
            #     'movie_name': items['nm'],
            #     'movie_type': items['cat'],
            #     'movie_region': items['src'],
            #     'movie_lang': items['oriLang'],
            #     'movie_score': float(items['sc']),
            #     'movie_release_time': items['rt'],
            #     'movie_videourl': items['videourl'],
            #     'movie_dra': items['dra']
            # })
            yield info

            # 获取上映时间，在爬取评论时做当前时间与上映时间的比较
            # self.release_time: items['rt']
        except Exception as e:
            self.logger.error(e)
