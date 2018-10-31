# -*- coding: utf-8 -*-
"""
多进程版爬虫
@file: multiprocess_version.py
@time: 2018/10/25 19:39
Created by Junyi.
"""
from multiprocessing import Pool
from .redis_queue import RedisQueue
from .normal_queue import NormalQueue
from .data_handler import get_crawl_urls
from .requests_helper import request_url, first_parse_response


class MultiProcessSpider(object):

    def __init__(self, queue_type):
        """
        :param queue_type: 共享队列类型(redis|normal|)
        """
        self.queue = self.__get_queue_object(queue_type)
        self.__init_spider()

    def __init_spider(self):
        crawl_urls = get_crawl_urls()
        self.queue.put_urls_in_queue(crawl_urls)

    def crawl(self):
        """
        一个子进程执行的爬取任务
        :return: None
        """
        while True:
            url = self.queue.get_url_from_queue()
            response = request_url(url)
            first_parsed_data = first_parse_response(response)
            new_urls = first_parsed_data['urls'] if first_parsed_data else None
            self.queue.put_urls_in_queue(new_urls)

    def start_crawl(self):
        """
        多进程调度函数
        :return: None
        """
        pool = Pool(processes=8)
        for _ in range(8):
            pool.apply_async(self.crawl, args=(self.queue, ))
        pool.close()
        pool.join()

    @staticmethod
    def __get_queue_object(queue_type):
        """
        获取共享url队列对象
        :param queue_type:采用队列的类型
        :return: ->queue object
        """
        if queue_type == 'redis':
            return RedisQueue()
        elif queue_type == 'normal':
            return NormalQueue()
        else:
            return None
