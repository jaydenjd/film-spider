# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MovieInfoItem(Item):
    collection = table = 'movie_info'
    movie_id = Field()
    movie_name = Field()
    movie_type = Field()
    movie_region = Field()
    movie_lang = Field()
    movie_score = Field()
    movie_release_time = Field()
    movie_videourl = Field()
    movie_dra = Field()
    # movie_info = Field()


class MovieCommentsItem(Item):
    collection = table = 'comments'
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
