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
        self.comments_url = 'http://m.maoyan.com/mmdb/comments/movie/{}.json?_v_=yes&offset=0&startTime=0' \
            .format(self.film_id)

    def start_requests(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 "
                          "Safari/537.36"
        }
        yield Request(self.movie_url, headers=headers, callback=self.parse_movie)

    def parse_movie(self, response):
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
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())).replace(' ', '%20')
            end_time = self.get_end_time()
            while start_time.split(' ')[0] > end_time:
                print('[INFO]: start time is %s...' % start_time.replace('%20', ' '))
                for page in range(67):
                    print('<Page>: %s', page)
                    headers = {
                        "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 "
                                      "Safari/537.36"

                    }

                    comments_url = 'http://m.maoyan.com/mmdb/comments/movie/{}.json?_v_=yes&offset={}&' \
                                        'startTime={}'.format(self.film_id, page * 15, start_time)

                    yield Request(comments_url, callback=self.parse_comments, headers=headers)
                start_time = start_time.replace('%20', ' ')
                start_time = datetime.datetime.fromtimestamp(
                    time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))) + datetime.timedelta(
                    seconds=-24 * 3600)
                start_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(time.mktime(start_time.timetuple()))).replace(' ', '%20')
            yield Request(self.comments_url, callback=self.parse_comments)


            # 获取上映时间，在爬取评论时做当前时间与上映时间的比较
            # self.release_time: items['rt']
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
            data = {}
            for item in items:
                comment['movie_id'] = item['movieId'] if 'movieId' in item else ''
                comment['comment_id'] = item['id']
                comment['nickName'] = item['nickName']
                # 可能没有性别的信息，'gender'为1代表男性，为2代表女性
                comment['gender'] = item['gender'] if 'gender' in item else 0
                # 可能没有所在城市的信息
                comment['cityName'] = item['cityName'] if 'cityName' in item else ''
                comment['score'] = float(item['score'])
                comment['content'] = item['content']
                comment['start_time'] = item['startTime']
                # 用户信息
                # comment['comments'] = {
                #     'movie_id': item['movieId'],
                #     'comment_id': item['id'],
                #     'nickName': item['nickName'],
                #     'gender': item['gender'] if 'gender' in item else '',
                #     'cityName': item['cityName'] if 'cityName' in item else '',
                #     'score': item['score'],
                #     'content': item['content'],
                #     'start_time': item['startTime'],
                # }

                yield comment


        except Exception as e:
            logging.error(e)

