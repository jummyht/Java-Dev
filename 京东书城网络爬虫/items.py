# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# items文件主要用来设置爬虫文件需要爬取的字段
# 这里主要有：书籍名称、书籍链接、价格、评论等

import scrapy


class JingdongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 商品ID
    thisid = scrapy.Field()
    # 商品标题
    title = scrapy.Field()
    # 商品链接
    cd_link = scrapy.Field()
    # 商品店家名字
    shop = scrapy.Field()
    # 商品店家连接
    shoplink = scrapy.Field()
    # 商品价格
    price = scrapy.Field()
    # 商品好评度
    comment = scrapy.Field()
    # 商品评论数
    com_count = scrapy.Field()
