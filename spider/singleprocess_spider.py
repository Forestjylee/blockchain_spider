# -*- coding: utf-8 -*-
"""
单进程版爬虫
@file: singleprocess_spider.py
@time: 2018/12/3 9:41
Created by Junyi.
"""
from .base_spider import BaseSpider


class SingleProcessSpider(BaseSpider):

    def __init__(self):
        super(SingleProcessSpider, self).__init__()

    def start_crawl(self):
        self.crawl()
