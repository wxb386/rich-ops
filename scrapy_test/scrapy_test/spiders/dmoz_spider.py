#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 18-11-28 上午11:17
# @Author  : wuxiangbin
# @Site    : www.rich-f.com
# @File    : dmoz_spider.py
# @Software: PyCharm
# @Function:
import scrapy


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        'https://www.bilibili.com/v/game/stand_alone/#/',
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
