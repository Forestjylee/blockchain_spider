# -*- coding: utf-8 -*-
"""
多进程版爬虫
@file: multiprocess_version.py
@time: 2018/10/25 19:39
Created by Junyi.
"""
from multiprocessing import Pool
from .base_spider import BaseSpider


class MultiProcessSpider(BaseSpider):
    """多进程爬虫(继承BaseSpider类)"""
    def __init__(self, process_num):
        """
        :param process_num: 同时执行的进程数
        """
        super(MultiProcessSpider, self).__init__()
        self.process_num = process_num

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
