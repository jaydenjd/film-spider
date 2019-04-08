# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import json
import logging
import uuid
from scrapy import Request, Spider
from ..settings import MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT
from ..items import DoubanMovieInfoItem, DoubanMovieCommentsItem
import pymysql

class DoubanmovieoneSpider(Spider):
    name = 'doubanMovieOne'
    allowed_domains = ['douban.com']

    def __init__(self, *args, **kwargs):
        super(DoubanmovieoneSpider, self).__init__(*args, **kwargs)
        self.movie_url = 'http://api.douban.com/v2/movie/subject/{}?apikey=0b2bdeda43b5688921839c8ecb20399b'
        self.comments_url = 'https://api.douban.com/v2/movie/subject/{film_id}/comments?apikey=0b2bdeda43b5688921839c8ecb20399b&start={offset}&count=30&client=&udid='

    def exc_sql(self):
        host = MYSQL_HOST
        database = MYSQL_DATABASE
        user = MYSQL_USER
        password = MYSQL_PASSWORD
        port = MYSQL_PORT
        db = pymysql.connect(host=host, user=user, password=password, db=database, port=port, charset='utf8mb4')
        cursor = db.cursor()
        query_sql = "SELECT movie_id FROM {}.douban_movie_request ORDER BY request_date DESC LIMIT 0,1".format(database)
        cursor.execute(query_sql)
        result = cursor.fetchone()
        db.close()
        return result

    def start_requests(self):
        result = self.exc_sql()
        film_id = str(result[0])
        movie_url = self.movie_url.format(film_id)
        # 通过meta将film_id传过去
        yield Request(movie_url, callback=self.parse_movie, meta={'film_id': str(film_id)})

    # 电影基本信息解析，并构建影评请求
    def parse_movie(self, response):
        info = DoubanMovieInfoItem()
        film_id = response.meta['film_id']
        try:
            # 将返回数据loads成字典
            items = json.loads(response.text)
            info['uuid'] = str(int(uuid.uuid3(uuid.NAMESPACE_DNS, str(items['title'])+str(items['pubdate']))))[0:9]
            # info['uuid'] = str(uuid.uuid1())
            info['movie_id'] = items['id']  # 猫眼电影Id
            info['name'] = items['title']  # 电影名字
            # if items['title'] != items['original_title']:
            #     info['enm'] = items['original_title']
            # elif items['title'] == items['original_title']:
            #     if len[items['aka']] == 1:
            #         info['enm'] = items['aka'][0]
            #     else:
            #         info['enm'] = items['aka'][-1]
            info['enm'] = items['original_title']
            info['type'] = ','.join(items['genres'])  # 电影类型,原本数据是个list类型，在此转为str
            info['region'] = items['countries']  # 电影地区
            info['lang'] = items['languages']  # 电影语言
            info['durations'] = items['durations']
            info['pubdate'] = items.get('pubdate', '')  # 电影上映时间
            info['data_from'] = '豆瓣'
            info['score'] = float(items['rating'].get('average'))  # 电影评分'
            # 导演信息
            directors = {}
            for director in items['directors']:
                director_avatar = director.get('avatars', {}).get('large', '')
                name = director.get('name', '')
                directors[name] = director_avatar
            info['directors'] = json.dumps(directors)
            # 演员信息
            actors = {}
            for actor in items['casts']:
                director_avatar = actor.get('avatars', {}).get('large', '')
                name = actor.get('name', '')
                actors[name] = director_avatar
            info['actors'] = json.dumps(actors)
            # 编剧信息
            writers = {}
            for writer in items['casts']:
                director_avatar = writer.get('avatars', {}).get('large', '')
                name = writer.get('name', '')
                writers[name] = director_avatar
            info['writers'] = json.dumps(writers)
            info['img'] = items.get('images', {}).get('large', '')  # 电影海报
            info['videourl'] = items.get('trailers', [])[0].get('resource_url', '')  # 电影宣传视频链接
            info['dra'] = items['summary']
            yield info
            for start in range(0, 17):
                comments_url = self.comments_url.format(film_id=film_id, offset=start * 30)
                yield Request(comments_url, callback=self.parse_comments,
                              meta={'source_url': comments_url, 'name': items['title'], 'pubdate': items['pubdate']})
        except Exception as e:
            logging.error(e)
            logging.error('+++++++++++++')

    # 影评解析
    def parse_comments(self, response):

        comment = DoubanMovieCommentsItem()
        try:
            items = json.loads(response.text).get('comments')
            source_url = response.meta['source_url']
            name = response.meta['name']
            pubdate = response.meta['pubdate']
            for item in items:
                # comment['uuid'] = str(uuid.uuid1())
                comment['uuid'] = str(int(uuid.uuid3(uuid.NAMESPACE_DNS, str(name) + str(pubdate))))[0:9]
                comment['movie_id'] = item['subject_id']  # 电影id
                comment['comment_id'] = item['id']  # 影评id
                comment['nickName'] = item.get('author', {}).get('name')  # 昵称
                # 可能没有性别的信息，'gender'为1代表男性，为2代表女性，如果不存在，则指定gender=0
                comment['gender'] = 'unkown'
                # 可能没有所在城市的信息
                comment['cityName'] = 'unknown'  # 所在城市
                comment['score'] = float(item.get('rating', {}).get('value', ''))  # 评分
                comment['content'] = item['content']  # 评论内容
                comment['date'] = item['created_at'].split(' ')[0]  # 评论时间
                comment['time'] = item['created_at'].split(' ')[1]  # 评论时间
                comment['data_from'] = '豆瓣'
                comment['source_url'] = source_url
                yield comment

        except Exception as e:
            logging.error(e)


