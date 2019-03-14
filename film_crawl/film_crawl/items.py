# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MovieInfoItem(Item):
    collection = table = 'movie_info'
    movie_id = Field()
    name = Field()
    enm = Field()
    type = Field()
    region = Field()
    lang = Field()
    score = Field()
    release_time = Field()
    img = Field()
    videourl = Field()
    dra = Field()
    info = Field()


class MovieCommentsItem(Item):
    collection = table = 'movie_comments'
    movie_id = Field()
    comment_id = Field()
    content = Field()
    cityName = Field()
    nickName = Field()
    gender = Field()
    start_time = Field()
    score = Field()


class RequestInfoItem(Item):
    collection = table = 'request_info'
    movie_id = Field()
    movie_name = Field()
