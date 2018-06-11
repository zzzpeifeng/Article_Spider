# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobboleArticleItem(scrapy.Item):
    front_img_url = scrapy.Field()
    front_img_path = scrapy.Field()
    title = scrapy.Field()
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    create_time = scrapy.Field()
    praise_num = scrapy.Field()
    fav_num = scrapy.Field()
    comment_num = scrapy.Field()
    conent = scrapy.Field()
    tags = scrapy.Field()
