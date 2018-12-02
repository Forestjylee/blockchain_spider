# -*- coding: utf-8 -*-
"""
start_urls_spider模块单元测试
@file: test_start_urls_spider.py
@time: 2018/12/2 21:37
Created by Junyi.
"""
from spider.start_urls_spider import get_start_urls


class TestStartUrlsSpider(object):

    def test_baidu_spider(self):
        for url in get_start_urls('baidu', '区块链', 10):
            print(url)

    def test_sogou_spider(self):
        for url in get_start_urls('sogou', '区块链', 10):
            print(url)

    def test_bing_spider(self):
        for url in get_start_urls('bing', '区块链', 10):
            print(url)
