# -*- coding: utf-8 -*-
import json
import logging
import re
import time
import datetime
import scrapy
from ..items import MovieCommentsItem
import requests


class MovieCommentsSpider(scrapy.Spider):
    name = 'film_comments'
    allowed_domains = ['m.maoyan.com']

    def __init__(self, film_id):
        self.film_id = film_id

    # 获得上映时间
    def get_end_time(self):
        film_url = 'https://maoyan.com/films/' + self.film_id
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 "
                          "Safari/537.36"

        }
        res = requests.get(film_url, headers=headers)
        end_time = re.findall(r'"ellipsis">(\d+-\d+-\d+).*?<', res.text)[0]
        return end_time

    def start_requests(self):

        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())).replace(' ', '%20')
        end_time = self.get_end_time()
        while start_time.split(' ')[0] > end_time:
            print('[INFO]: start time is %s...' % start_time.replace('%20', ' '))
            for page in range(67):
                print('<Page>: %s', page)
                start_urls = 'http://m.maoyan.com/mmdb/comments/movie/{}.json?_v_=yes&offset={}&startTime={}' \
                    .format(self.film_id, page * 15, start_time)
                yield scrapy.Request(start_urls, callback=self.parse)
            start_time = start_time.replace('%20', ' ')
            start_time = datetime.datetime.fromtimestamp(
                time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))) + datetime.timedelta(seconds=-1 * 3600)
            start_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                       time.localtime(time.mktime(start_time.timetuple()))).replace(' ', '%20')

    def parse(self, response):
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
