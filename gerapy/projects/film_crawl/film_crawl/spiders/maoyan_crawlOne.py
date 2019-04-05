import datetime
import json
import logging
import time
from scrapy import Request, Spider
from ..settings import MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT
# from ..items import MovieInfoItem, MovieCommentsItem
import pymysql


class MaoyanCrawlOneSpider(Spider):
    name = 'maoyan_crawlOne'
    allowed_domains = ['maoyan.com']

    def __init__(self, *args, **kwargs):
        super(MaoyanCrawlOneSpider, self).__init__(*args, **kwargs)
        self.movie_url = 'http://api.maoyan.com/mmdb/movie/v5/{}.json'
        self.comments_url = 'http://m.maoyan.com/mmdb/comments/movie/{film_id}.json?_v_=yes&' \
                            'offset={offset}&startTime={start_time}'

    # def exc_sql(self):
    #     host = MYSQL_HOST
    #     database = MYSQL_DATABASE
    #     user = MYSQL_USER
    #     password = MYSQL_PASSWORD
    #     port = MYSQL_PORT
    #     db = pymysql.connect(host=host, user=user, password=password, db=database, port=port, charset='utf8mb4')
    #     cursor = db.cursor()
    #     query_sql = "SELECT movie_id FROM film_spider.request_info ORDER BY  request_date DESC LIMIT 0,1"
    #     cursor.execute(query_sql)
    #     result = cursor.fetchone()
    #     db.close()
    #     return result
    #
    # def start_requests(self):
    #     result = self.exc_sql()
    #     film_id = str(result[0])
    #     movie_url = self.movie_url.format(film_id)
    #     # 通过meta将film_id传过去
    #     yield Request(movie_url, callback=self.parse_movie, meta={'film_id': str(film_id)})
    #
    # # 电影基本信息解析，并构建影评请求
    # def parse_movie(self, response):
    #     info = MovieInfoItem()
    #     film_id = response.meta['film_id']
    #     try:
    #         # 将返回数据loads成字典
    #         items = json.loads(response.text).get('data').get('movie')
    #         info['movie_id'] = items['id']  # 电影Id
    #         info['name'] = items['nm']  # 电影名字
    #         info['enm'] = items['enm']  # 电影英文名
    #         info['type'] = items['cat']  # 电影类型
    #         info['region'] = items['src']  # 电影地区
    #         info['lang'] = items['oriLang']  # 电影语言
    #         info['score'] = float(items['sc'])  # 电影评分
    #         info['release_time'] = items['rt']  # 电影上映时间
    #         # 原url是无效链接，要去到原url中的'/w.h'字符串才是有效链接，并且将Http协议改成https安全协议
    #         info['img'] = items['img'].replace('http', 'https').replace('/w.h', '')  # 电影海报
    #         info['videourl'] = items['videourl']  # 电影宣传视频链接
    #         info['dra'] = items['dra']  # 电影简介
    #         info['info'] = json.dumps(
    #             {'movie_id': items['id'], 'name': items['nm'], 'enm': items['enm'], 'type': items['cat'],
    #              'region': items['src'], 'lang': items['oriLang'], 'score': float(items['sc']),
    #              'release_time': items['rt'], 'img': items['img'].replace('http', 'https').replace('/w.h', ''),
    #              'videourl': items['videourl']})
    #         yield info
    #         # 影评接口中的start_time是评论时间，在接口中需要在日期后面、小时前面加'%20'才是有效的
    #         start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())).replace(' ', '%20')
    #         # 获取电影上映时间
    #         end_time = items['rt']
    #         # 判断评论时间要早于上映时间，才开始进行爬取
    #         while start_time.split(' ')[0] > end_time:
    #             # 可以指定一个时间来让进程挂起，以免过于频繁访问
    #             # time.sleep(1)
    #             # print('[INFO]: start time is %s...' % start_time.replace('%20', ' '))
    #             # logging.info('start time is %s...' % start_time.replace('%20', ' '))
    #             # 每一个特定的start_time，只有offset=66*15=990条可抓取评论数，到了offset=1050后，返回数据为空
    #             for page in range(67):
    #                 # logging.info('上映时间' + end_time)
    #                 # 通过传入film_id,offset,start_time构建影评API
    #                 comments_url = self.comments_url.format(film_id=film_id, offset=page * 15,
    #                                                         start_time=start_time)
    #                 # 构建影评请求并返回影评请求结果，指定回调参数为影评解析函数
    #                 yield Request(comments_url, callback=self.parse_comments, meta={'source_url': comments_url})
    #             # 通过改变start_time来获取更多影评数据
    #             start_time = start_time.replace('%20', ' ')
    #             start_time = datetime.datetime.fromtimestamp(
    #                 time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))) + datetime.timedelta(
    #                 seconds=-1 * 3600)
    #             start_time = time.strftime('%Y-%m-%d %H:%M:%S',
    #                                        time.localtime(time.mktime(start_time.timetuple()))).replace(' ', '%20')
    #     except Exception as e:
    #         logging.error(e)
    #
    # # 影评解析
    # def parse_comments(self, response):
    #     comment = MovieCommentsItem()
    #     try:
    #         items = json.loads(response.text).get('cmts')
    #         source_url = response.meta['source_url']
    #         for item in items:
    #             comment['movie_id'] = item['movieId']  # 电影id
    #             comment['comment_id'] = item['id']  # 影评id
    #             comment['nickName'] = item['nickName']  # 昵称
    #             # 可能没有性别的信息，'gender'为1代表男性，为2代表女性，如果不存在，则指定gender=0
    #             comment['gender'] = str(item['gender']) if 'gender' in item else '0'  # 性别
    #             # 可能没有所在城市的信息
    #             comment['cityName'] = item['cityName'] if 'cityName' in item else 'unknown'  # 所在城市
    #             comment['score'] = float(item['score'])  #评分
    #             comment['content'] = item['content']  # 评论内容
    #             comment['date'] = item['startTime'].split(' ')[0]  # 评论时间
    #             comment['time'] = item['startTime'].split(' ')[1]  # 评论时间
    #             comment['source_url'] = source_url
    #             yield comment
    #
    #     except Exception as e:
    #         logging.error(e)
