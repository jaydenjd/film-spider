# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MovieInfoItem(Item):
    collection = table = 'movie_info'
    movie_id = Field()  # 电影id
    name = Field()  # 电影名称
    enm = Field()   # 电影英文名称
    type = Field()  # 电影类型
    region = Field()    # 电影地区
    lang = Field()  # 电影语言
    score = Field()  # 电影平均分
    release_time = Field()  # 电影上映时间
    img = Field()   # 电影海报图片
    videourl = Field()  # 电影宣传电影
    dra = Field()   # 电影简介
    info = Field()  # 电影部分信息


class MovieCommentsItem(Item):
    collection = table = 'movie_comments'
    movie_id = Field()
    comment_id = Field()
    nickName = Field()
    gender = Field()
    cityName = Field()
    score = Field()
    content = Field()
    date = Field()
    time = Field()
    source_url = Field()


class RequestInfoItem(Item):
    collection = table = 'request_info'
    movie_id = Field()
    movie_name = Field()
    request_date = Field()
    region = Field()
    create_date = Field()
