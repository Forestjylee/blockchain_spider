# -*- coding: utf-8 -*-
"""
多进程版爬虫
@file: multiprocess_version.py
@time: 2018/10/25 19:39
Created by Junyi.
"""
from multiprocessing import Pool
from utils.log_helper import get_logger
from utils.parse_helper import ParseHelper
from utils.requests_helper import request_url
from .start_urls_spider import get_more_start_urls


class MultiProcessSpider(object):

    def __init__(self, queue, pipline, process_num):
        """
        :param process_num: 同时执行的进程数
        :param queue: 共享队列对象(redis|...|)
        :param pipline: 输送到数据库的管道对象
        :parameter logger: 日志生成对象，默认过滤级别为logging.INFO
        """
        self.process_num = process_num
        self.queue = queue
        self.pipline = pipline
        self.logger = get_logger('blockchain_spider', to_file=True, filename='spider')

    def crawl(self):
        """
        一个子进程执行的爬取任务
        流程：
        1.从共享url队列中取出一个url, 若无则使用搜索引擎获取更多起始地址
        2.使用request_url函数获取网页response
        3.使用ParseHelper中的解析函数解析网页
        4.将数据存储到MongoDB数据库中
        5.将网页中解析出来的url放入共享队列
        6.记录日志
        [此方案需可以改进的地方：将request请求url部分与后续处理部分分离，
        采用异步HTTP请求的方式进一步爬取提高效率(1,2)(3,4,5)分离]
        :return: None
        """
        while True:
            url = self.queue.get_url_from_queue()
            response = request_url(url) if url else get_more_start_urls()
            first_parsed_data = ParseHelper.first_parse_response(response)
            new_urls = first_parsed_data['urls'] if first_parsed_data else None
            self.pipline.save_html_data(first_parsed_data)
            url_amount = self.queue.put_urls_in_queue(new_urls)
            self.logger.info(f"{url} is crawled.")
            self.logger.info(f"There are {url_amount} urls in queue now.")

    def start_crawl(self):
        """
        多进程调度函数(进程池实现)
        :return: None
        """
        self.logger.info(f"Start with {self.queue.get_queue_len()} urls in queue.")
        pool = Pool(processes=self.process_num)
        for _ in range(self.process_num):
            pool.apply_async(self.crawl, args=(self.queue, ))
        pool.close()
        pool.join()
