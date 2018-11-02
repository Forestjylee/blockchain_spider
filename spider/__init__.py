# -*- coding: utf-8 -*-
"""
spider包
爬取有关区块链的数据
@file: __init__.py
@time: 2018/10/22 10:48
Created by Junyi.
"""
from url_queue import get_queue_object
from .multiprocess_spider import MultiProcessSpider
from .start_urls_spider import get_start_urls, build_start_urls_pool


def run_spider(keyword, queue_type='redis'):
    """
    爬虫的入口函数
    默认使用redis作为url共享队列
    :param keyword: 爬取的关键字
    :param queue_type: url共享队列类型
    :return: None
    """
    queue = get_queue_object(queue_type)
    if queue.is_queue_empty():
        build_start_urls_pool(keyword, queue)
    spider = MultiProcessSpider(queue)
    spider.start_crawl()


def run_test_spider(keyword):
    #TODO 用于展示和测试网络环境的爬虫
    pass
