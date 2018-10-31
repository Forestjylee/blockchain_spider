# -*- coding: utf-8 -*-
"""
多进程版爬虫
@file: multiprocess_version.py
@time: 2018/10/25 19:39
Created by Junyi.
"""
from multiprocessing import Pool
from utils.parse_helper import ParseHelper
from utils.requests_helper import request_url
from url_queue.redis_queue import RedisQueue
from url_queue.normal_queue import NormalQueue
from pipline.mongo_pipline import MongoPipline

class MultiProcessSpider(object):

    def __init__(self, queue_type, process_num=6):
        """
        :param process_num: 同时执行的进程数
        :param queue_type: 共享队列类型(redis|normal|)
        """
        self.process_num = process_num
        self.queue = self.__get_queue_object(queue_type)
        self.mongo_tube = MongoPipline()
        self.__init_spider(queue_type)

    def __init_spider(self, queue_type):
        """
        初始化爬虫队列
        :param queue_type: 共享队列类型(redis|normal|)
        :return: None
        """
        if queue_type == 'normal':
            crawl_urls = self.mongo_tube.get_crawl_urls()
            self.queue.put_urls_in_queue(crawl_urls)

    def crawl(self):
        """
        一个子进程执行的爬取任务
        :return: None
        """
        while True:
            url = self.queue.get_url_from_queue()
            response = request_url(url)
            first_parsed_data = ParseHelper.first_parse_response(response)
            new_urls = first_parsed_data['urls'] if first_parsed_data else None
            self.queue.put_urls_in_queue(new_urls)

    def start_crawl(self):
        """
        多进程调度函数(进程池实现)
        :return: None
        """
        pool = Pool(processes=self.process_num)
        for _ in range(self.process_num):
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
