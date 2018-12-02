# -*- coding: utf-8 -*-
"""
多进程版爬虫
@file: multiprocess_version.py
@time: 2018/10/25 19:39
Created by Junyi.
"""
from multiprocessing import Pool
from pipline import get_pipline_object
from url_queue import get_queue_object
from utils.log_helper import get_logger
from utils.parse_helper import ParseHelper
from utils.requests_helper import request_url
from settings import (
    KEYWORD,
    URL_QUEUE_TYPE,
    PIPLINE_TYPE,
    PROCESS_NUMBER,
    TIMEOUT,
    SPIDER_LOG_NAME,
)


class MultiProcessSpider(object):

    def __init__(self):
        """
        :param keyword: 爬取的关键字
        :param process_num: 同时执行的进程数
        :param url_queue_type: 共享队列类型(redis|...|)
        :param pipline_type: 输送到数据库的管道类型
        :param timeout: 单次HTTP request超时时间(默认为None，永久等待)
        :param spider_log_name: 爬虫日志的文件名
        """
        self.keyword = KEYWORD
        self.url_queue_type = URL_QUEUE_TYPE
        self.pipline_type = PIPLINE_TYPE
        self.process_num = PROCESS_NUMBER
        self.timeout = TIMEOUT
        self.spider_log_name = SPIDER_LOG_NAME

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
        :parameter logger: 日志生成对象，默认过滤级别为logging.INFO
        :return: None
        """
        queue = get_queue_object(self.url_queue_type)
        pipline = get_pipline_object(self.pipline_type)
        logger = get_logger(
            "blockchain_spider", to_file=True, filename=self.spider_log_name
        )
        while True:
            url = queue.get_url_from_queue()
            response = request_url(url, timeout=self.timeout)
            first_parsed_data = ParseHelper.first_parse_response(
                response, keyword=self.keyword
            )
            new_urls = first_parsed_data["urls"] if first_parsed_data else None
            pipline.save_html_data(first_parsed_data)
            url_amount = queue.put_urls_in_queue(new_urls)
            logger.info(f"{url} has been crawled.")
            if url_amount:
                logger.info(f"There are {url_amount} urls in queue now.")

    def start_crawl(self):
        """
        多进程调度函数(进程池实现)
        :return: None
        """
        pool = Pool(processes=self.process_num)
        for _ in range(self.process_num):
            pool.apply_async(self.crawl)
        pool.close()
        pool.join()
