# -*- coding: utf-8 -*-
"""
多进程版爬虫
@file: multiprocess_version.py
@time: 2018/10/25 19:39
Created by Junyi.
"""
from multiprocessing import Pool
from url_queue import get_queue_object
from utils.parse_helper import ParseHelper
from utils.requests_helper import request_url
from pipline.mongo_pipline import MongoPipline
# TODO logging日志模块初步定于在此添加

class MultiProcessSpider(object):

    def __init__(self, queue_type, process_num=6):
        """
        :param process_num: 同时执行的进程数
        :param queue_type: 共享队列类型(redis|normal|)
        """
        self.process_num = process_num
        self.queue = get_queue_object(queue_type)
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
        流程：
        1.从共享url队列中取出一个url
        2.使用request_url函数获取网页response
        3.使用ParseHelper中的解析函数解析网页
        4.将数据存储到MongoDB数据库中
        5.将网页中解析出来的url放入共享队列
        [此方案需可以改进的地方：将request请求url部分与后续处理部分分离，
        采用异步HTTP请求的方式进一步爬取提高效率(1,2)(3,4,5)分离]
        :return: None
        """
        while True:
            url = self.queue.get_url_from_queue()
            response = request_url(url)
            first_parsed_data = ParseHelper.first_parse_response(response)
            new_urls = first_parsed_data['urls'] if first_parsed_data else None
            MongoPipline.save_html_data_to_mongo(first_parsed_data)
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
