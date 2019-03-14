# -*- coding: utf-8 -*-
import datetime
import json
import logging
import re
import time
import requests
from scrapy import Request, Spider

from ..items import MovieInfoItem, MovieCommentsItem


class MaoyanSpider(Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']

    def __init__(self, film_id):
        self.film_id = film_id
        self.movie_url = 'http://api.maoyan.com/mmdb/movie/v5/{}.json'.format(self.film_id)
        self.comments_url = 'http://m.maoyan.com/mmdb/comments/movie/{}.json?_v_=yes&offset={}&startTime={}'

    def start_requests(self):
        yield Request(self.movie_url, callback=self.parse_movie)

    def parse_movie(self, response):
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
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())).replace(' ', '%20')
            end_time = self.get_end_time()
            while start_time.split(' ')[0] > end_time:
                # time.sleep(1)
                print('[INFO]: start time is %s...' % start_time.replace('%20', ' '))
                for page in range(67):
                    comments_url = self.comments_url.format(self.film_id, page * 15, start_time)

                    yield Request(comments_url, callback=self.parse_comments)
                start_time = start_time.replace('%20', ' ')
                start_time = datetime.datetime.fromtimestamp(
                    time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))) + datetime.timedelta(
                    seconds=-1 * 3600)
                start_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(time.mktime(start_time.timetuple()))).replace(' ', '%20')
        except Exception as e:
            logging.error(e)

    def get_end_time(self):
        film_url = 'https://maoyan.com/films/' + self.film_id
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 "
                          "Safari/537.36"

        }
        res = requests.get(film_url, headers=headers)
        end_time = re.findall(r'"ellipsis">(\d+-\d+-\d+).*?<', res.text)[0]
        return end_time

    def parse_comments(self, response):
        comment = MovieCommentsItem()
        try:
            items = json.loads(response.text).get('cmts')
            for item in items:
                comment['movie_id'] = item['movieId']
                comment['comment_id'] = item['id']
                comment['nickName'] = item['nickName']
                # 可能没有性别的信息，'gender'为1代表男性，为2代表女性
                comment['gender'] = item['gender'] if 'gender' in item else 0
                # 可能没有所在城市的信息
                comment['cityName'] = item['cityName'] if 'cityName' in item else ''
                comment['score'] = float(item['score'])
                comment['content'] = item['content']
                comment['start_time'] = item['startTime']
                yield comment

        except Exception as e:
            logging.error(e)
