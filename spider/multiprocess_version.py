# -*- coding: utf-8 -*-
"""
多进程版爬虫
@file: multiprocess_version.py
@time: 2018/10/25 19:39
Created by Junyi.
"""
from multiprocessing import Manager, Pool
from .requests_helper import request_url, first_parse_response
from .data_handler import get_crawl_urls

#TODO redis数据库代替队列Queue

def crwal(queue, lock):
    """
    一个子进程执行的爬取任务
    :param queue: 共享url队列
    :param lock: 锁变量
    :return: None
    """
    while True:
        url = get_url_from_queue(queue)
        response = request_url(url)
        first_parsed_data = first_parse_response(response)
        new_urls = first_parsed_data['urls'] if first_parsed_data else None
        put_urls_in_queue(queue, lock, new_urls)


def put_urls_in_queue(queue, lock, urls):
    """
    将列表中的url放入队列
    :param queue: 共享url队列
    :param lock: 锁变量
    :param urls: 需要插入的url
    :return: None
    """
    if urls:
        lock.acquire()
        for url in urls:
            queue.put(url)
        lock.release()


def get_url_from_queue(queue):
    """
    从队列中获取1个url
    :param queue: 共享url队列
    :return: ->url(str)
    """
    while True:
        if not queue.empty():
            url = queue.get()
            if url:
                return url


def multiprocess_crawl():
    """
    多进程调度函数
    :return: None
    """
    manager = Manager()
    lock = manager.Lock()
    queue = manager.Queue()
    crawl_urls = get_crawl_urls()
    put_urls_in_queue(queue, lock, crawl_urls)
    pool = Pool(processes=8)
    for _ in range(8):
        pool.apply_async(crwal, args=(queue, lock, ))
    pool.close()
    pool.join()



