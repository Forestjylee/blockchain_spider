# -*- coding: utf-8 -*-
"""
展示版爬虫
1.不记录日志
2.不保存数据
3.开启共享队列
@file: presentation_spider.py
@time: 2018/12/3 10:27
Created by Junyi.
"""
from pprint import pprint
from multiprocessing import Pool
from .base_spider import BaseSpider


class PresentationSpider(BaseSpider):

    def __init__(self, process_num):
        super(PresentationSpider, self).__init__()
        self.process_num = process_num

    def crawl(self):
        queue = self._get_queue_object()
        while True:
            url = queue.get_url_from_queue()
            response = self._request_url(url)
            first_parsed_data = self._parse_response(response)
            new_urls = self._extract_new_urls(first_parsed_data)
            queue.put_urls_in_queue(new_urls)
            if first_parsed_data:
                pprint(first_parsed_data)
            else:
                print(f"{url}中没有关键字[>>>区块链<<<]!")

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

