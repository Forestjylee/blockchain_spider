# -*- coding: utf-8 -*-
"""
spider包
爬取有关区块链的数据
@file: __init__.py
@time: 2018/10/22 10:48
Created by Junyi.
"""
from url_queue import get_queue_object
from settings import (KEYWORD, URL_QUEUE_TYPE,
                      IGNORE_EXCEPTIONS, CRAWL_SPEED)  # TODO 根据爬取速度调节并行进程数
from utils.decorator import ensure_network_env, deal_exceptions
from .multiprocess_spider import MultiProcessSpider
from .start_urls_spider import get_start_urls, build_start_urls_pool


def spider_run():
    """爬取过程中遇到异常是否停止爬取"""
    if IGNORE_EXCEPTIONS:
        while 1:
            run()
    else:
        run()


@deal_exceptions(print_exceptions=True)
@ensure_network_env
def run():
    """
    爬虫的入口函数
    默认使用redis作为url共享队列
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    执行流程：
    1.测试网络是否通畅（装饰器实现）
    2.获取队列对象和数据库对象
    3.判断队列是否为空，构建起始地址池
    4.启动爬虫
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :return: None
    """
    queue = get_queue_object(URL_QUEUE_TYPE)
    print("数据库连接成功！\n正在获取起始地址池...")
    if queue.is_queue_empty():
        build_start_urls_pool(KEYWORD, queue)
    print("起始地址池构建成功，开始爬取...")
    spider = MultiProcessSpider()
    spider.start_crawl()
