# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanItem(scrapy.Item):
    # define the fields for your item here :
    movie_id = scrapy.Field()
    MovieName = scrapy.Field()
    MovieNameOther = scrapy.Field()
    MoviePost = scrapy.Field()
    MovieType = scrapy.Field()
    ReleasedDate = scrapy.Field()
    ReleasedArea = scrapy.Field()
    MovieNation = scrapy.Field()
    MovieDirector = scrapy.Field()
    ScreenWriter = scrapy.Field()
    DistributionEnterpris = scrapy.Field()
    MoviePlot = scrapy.Field()
    ReleasedYear = scrapy.Field()
    WantSeeNum = scrapy.Field()
    MarkNum = scrapy.Field()
    Score = scrapy.Field()
    TrailerNum = scrapy.Field()
    ActorNum = scrapy.Field()
    ImageNum = scrapy.Field()
    CommentNum = scrapy.Field()

    Movie_url = scrapy.Field()
    TrailerUrl = scrapy.Field()
    ActorUrl = scrapy.Field()
    ImageUrl = scrapy.Field()
    CommentUrl = scrapy.Field()
    CommentShortUrl = scrapy.Field()
    NewsNum = scrapy.Field()
    NewsUrl = scrapy.Field()

