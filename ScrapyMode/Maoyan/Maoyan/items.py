# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanShowItem(scrapy.Item):
    # define the fields for your item here :
    # 放映情况的数据表结构
    show_id = scrapy.Field()
    cinema_id = scrapy.Field()
    movie_id = scrapy.Field()
    show_date = scrapy.Field()
    begin_time = scrapy.Field()
    end_time = scrapy.Field()
    language = scrapy.Field()
    hall = scrapy.Field()
    pos = scrapy.Field()
    creation_date = scrapy.Field()
    last_update_time = scrapy.Field()


class MaoyanMovieItem(scrapy.Item):
    # define the fields for your item here :
    movie_name = scrapy.Field()


class MaoyanCelebrityItem(scrapy.Item):
    # define the fields for your item here :
    pass


class MaoyanCinemaItem(scrapy.Item):
    # define the fields for your item here :
    # name = scrapy.Field()
    pass


class MaoyanCinemaItem(scrapy.Item):
    # define the fields for your item here :
    # name = scrapy.Field()
    pass


class MaoyanCityItem(scrapy.Item):
    # define the fields for your item here :
    # name = scrapy.Field()
    pass