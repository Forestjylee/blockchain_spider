# -*- coding: utf-8 -*-
"""
爬虫的起始url
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
e.g.: start_urls = get_start_urls('baidu', '区块链', 30)
Get 30 start_urls about '区块链' from baidu.
备注：bing网站存在一定反爬措施，使得多次请求无法得到结果
     实际操作中尽量不要过多使用bing进行搜索。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@file: start_urls.py
@time: 2018/10/22 10:53
Created by Junyi.
"""
from threading import Thread, Lock
from utils.decorator import to_pickle
from .settings import (BAIDU_URL_TEMPLATE, SOGOU_URL_TEMPLATE,
                       BING_URL_TEMPLATE)
from utils.start_urls_helper import (parse_baidu_response, parse_sogou_response,
                                     parse_bing_response, get_target_start_urls,
                                     __put_in_pool)


def get_baidu_start_urls(keyword, amount):
    """
    通过百度的搜索结果，获取起始地址池
    :param keyword: 关键词
    :param amount；需要起始url的数量
    :return: ->start_urls(list)
    """
    start_urls = get_target_start_urls(BAIDU_URL_TEMPLATE, keyword,
                                       parse_baidu_response, amount)
    return start_urls


def get_sogou_start_urls(keyword, amount):
    """
    通过搜狗的搜索结果，获取起始地址池
    :param keyword: 关键词
    :param amount: 需要起始url的数量
    :return: ->start_urls(list)
    """
    start_urls = get_target_start_urls(SOGOU_URL_TEMPLATE, keyword,
                                       parse_sogou_response, amount)
    return start_urls


def get_bing_start_urls(keyword, amount):
    """
    通过必应国内版的搜索结果，获取起始地址池
    :param keyword: 关键词
    :param amount: 需要起始url的数量
    :return: ->start_urls(list)
    """
    start_urls = get_target_start_urls(BING_URL_TEMPLATE, keyword,
                                       parse_bing_response, amount)
    return start_urls


def get_start_urls(search_engine, keyword, amount=10):
    """
    顶层封装，供外部调用
    :param search_engine: 使用搜索引擎的类型(baidu, sogou, bing)
    :param keyword: 搜索关键字
    :param amount: 需要起始url的数量(默认为10)
    :return: ->start_urls(list)
    """
    if search_engine == 'baidu':
        return get_baidu_start_urls(keyword, amount)
    elif search_engine == 'sogou':
        return get_sogou_start_urls(keyword, amount)
    elif search_engine == 'bing':
        return get_bing_start_urls(keyword, amount)
    else:
        raise AttributeError


@to_pickle('start_urls.pck', print_result=True)
def build_start_urls_pool(keyword, queue_object=None,
                          baidu_num=50, sogou_num=50):
    """
    创建起始地址池
    多非守护式线程实现
    采用锁保证线程安全
    将结果序列化保存到运行目录下，以便后续恢复
    :param keyword: 搜索关键词
    :param queue_object: 队列对象(若无则不将结果放入队列)
    :param baidu_num: 从百度搜索中提取的起始地址数（默认100个）
    :param sogou_num: 从搜狗搜索中提取的起始地址数（默认100个）
    :return: ->start_urls<list>
    """
    start_urls = []
    lock = Lock()
    thread1 = Thread(target=__crawl_start_urls,
                     args=(start_urls, 'baidu',
                           keyword, baidu_num, lock))
    thread2 = Thread(target=__crawl_start_urls,
                     args=(start_urls, 'sogou',
                           keyword, sogou_num, lock))
    thread1.setDaemon(False)
    thread2.setDaemon(False)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    start_urls = list(set(start_urls))
    return __put_in_pool(start_urls, queue_object)


def __crawl_start_urls(start_urls, search_engine, keyword, amount, lock):
    """
    线程执行的任务
    :param start_urls: 起始地址列表
    :param search_engine: 使用的搜索引擎
    :param keyword: 搜索关键字
    :param amount: 需要的预期结果数量
    :param lock: 线程锁变量<threading.Lock>
    :return: None
    """
    for urls in get_start_urls(search_engine, keyword, amount):
        with lock:
            start_urls.extend(urls)
        print(urls)
