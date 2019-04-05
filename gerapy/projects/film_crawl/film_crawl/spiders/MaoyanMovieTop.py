# -*- coding: utf-8 -*-
import scrapy


class MaoyanmovietopSpider(scrapy.Spider):
    name = 'MaoyanMovieTop'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    def parse(self, response):
        pass
