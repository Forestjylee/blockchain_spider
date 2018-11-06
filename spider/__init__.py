# -*- coding: utf-8 -*-
"""
spider包
爬取有关区块链的数据
@file: __init__.py
@time: 2018/10/22 10:48
Created by Junyi.
"""
from url_queue import get_queue_object
from utils.decorator import ensure_network_env
from .multiprocess_spider import MultiProcessSpider
from .start_urls_spider import get_start_urls, build_start_urls_pool


@ensure_network_env
def run_spider(keyword, queue_type='redis', pipline_type='mongo', process_num=7, timeout=None):
    """
    爬虫的入口函数
    默认使用redis作为url共享队列
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~执行流程：                       ~
    ~1.测试网络是否通畅（装饰器实现）   ~
    ~2.获取队列对象和数据库对象        ~
    ~3.判断队列是否为空，构建起始地址池 ~
    ~4.启动爬虫                       ~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :param keyword: 爬取的关键字
    :param queue_type: url共享队列类型（默认redis）
    :param pipline_type: 使用的存储数据库管道类型（默认MongoDB）
    :param process_num: 并行进程数（默认为7）
    :param timeout: 单次请求超时时间(默认为None，永久等待)
    :return: None
    """
    queue = get_queue_object(queue_type)
    print("数据库连接成功！\n正在获取起始地址池...")
    if queue.is_queue_empty():
        build_start_urls_pool(keyword, queue)
    print("起始地址池构建成功，开始爬取...")
    spider = MultiProcessSpider(keyword, queue_type, pipline_type,
                                process_num, timeout)
    spider.start_crawl()
