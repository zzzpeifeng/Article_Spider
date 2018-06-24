# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime
from scrapy.loader import ItemLoader
import re


class ArticleSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value + "-jobbole"


def return_value(value):
    return value


def date_convert(value):
    try:
        create_date_result = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        create_date_result = datetime.datetime.now()
    return create_date_result


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


# 自定义Itemloader
class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    pass


class JobboleArticleItem(scrapy.Item):
    front_img_url = scrapy.Field(
        output_processor=MapCompose()
    )
    front_img_path = scrapy.Field()
    title = scrapy.Field(
        input_processor=MapCompose(add_jobbole)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    create_time = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    praise_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
