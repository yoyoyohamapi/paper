# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 服装
class YohoItem(scrapy.Item):
    # 所属搭配
    matching = scrapy.Field()
    # 分类:上装?下装?
    category = scrapy.Field()
    # 服饰风格
    style = scrapy.Field()
    # 图片
    img_url = scrapy.Field()
    # 商品URL
    product_url = scrapy.Field()
