# -*- coding: utf-8 -*-
"""
基本爬虫逻辑
@file: base_spider.py
@time: 2018/12/3 9:33
Created by Junyi.
"""
from pipline import get_pipline_object
from url_queue import get_queue_object
from utils.log_helper import get_logger
from utils.parse_helper import ParseHelper
from utils.requests_helper import request_url
from settings import (
    KEYWORD,
    URL_QUEUE_TYPE,
    PIPLINE_TYPE,
    TIMEOUT,
    SPIDER_LOG_NAME,
)


class BaseSpider(object):

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
        self.timeout = TIMEOUT
        self.spider_log_name = SPIDER_LOG_NAME

    def _get_queue_object(self):
        """获取共享队列对象"""
        return get_queue_object(self.url_queue_type)

    def _get_pipline_object(self):
        """获取数据管道对象"""
        return get_pipline_object(self.pipline_type)

    def _get_spider_logger(self):
        """获取爬虫日志对象"""
        return get_logger("spider", to_file=True, to_console=True,
                          filename=self.spider_log_name)

    def _request_url(self, url):
        """向url发出HTTP GET请求并返回response"""
        return request_url(url, self.timeout)

    def _parse_response(self, response):
        """解析request得到的response"""
        first_parsed_data = ParseHelper.first_parse_response(response, self.keyword)
        return first_parsed_data

    @staticmethod
    def _extract_new_urls(parsed_data):
        """从解析好的数据字典中提取指向网页外部的链接"""
        return parsed_data["urls"] if parsed_data else None

    def crawl(self):
        """
        单个进程执行的爬取任务
        准备阶段：
        1.创建共享队列对象
        2.创建数据管道对象
        3.创建爬虫日志对象
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
        queue = self._get_queue_object()
        pipline = self._get_pipline_object()
        logger = self._get_spider_logger()
        while True:
            url = queue.get_url_from_queue()
            response = self._request_url(url)
            first_parsed_data = self._parse_response(response)
            new_urls = self._extract_new_urls(first_parsed_data)
            pipline.save_html_data(first_parsed_data)
            queue.put_urls_in_queue(new_urls)
            logger.info(f"{url} has been crawled.")
