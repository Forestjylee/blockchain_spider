# -*- coding: utf-8 -*-
"""
测试爬虫基类
@file: test_spider.py
@time: 2018/12/3 11:09
Created by Junyi.
"""
from pprint import pprint
from spider.base_spider import BaseSpider


def test_base_spider():
    base_spider = BaseSpider()
    pprint(base_spider.__dict__)
    urls = ['http://www.bcfans.com/', 'http://www.dayqkl.com/', 'http://www.qukuainews.cn/',
            'http://news.sogou.com/news?mode=1&sort=0&fixrank=1&query=%C7%F8%BF%E9%C1%B4&shid=djt',
            'http://finance.china.com.cn/money/insurance/special/2018insurance-summit/20181203/4826394.shtml',
            'http://www.dsb.cn/t/1318', 'http://www.lianmenhu.com/', 'http://qukuaiwang.com.cn/']
    for url in urls:
        response = base_spider._request_url(url)
        first_parsed_data = base_spider._parse_response(response)
        pprint(first_parsed_data)
