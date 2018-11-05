# -*- coding: utf-8 -*-
"""
与数据库的交互部分
@file: data_handler.py
@time: 2018/10/25 19:42
Created by Junyi.
"""
import pymongo
from utils.decorator import deal_exceptions


class MongoPipline(object):

    def __init__(self):
        self.__client = pymongo.MongoClient('localhost')

    def get_crawl_urls(self, db_name='blockchain_data',
                       collection_name='crawl_urls'):
        """
        从MongoDB中取出url
        :param db_name: 数据库的名字
        :param collection_name: 表的名字
        :return: ->crawl_urls<list>
        """
        crawl_urls = []
        db = self.__client[db_name]
        for item in db[collection_name].find():
            crawl_urls.append(item['url'])
        return crawl_urls

    def save_crawl_urls(self, crawl_urls, db_name='blockchain_data',
                                 collection_name='crawl_urls'):
        """
        先删除原来的数据
        再将队列中的url保存至mongoDB中
        :param crawl_urls: 共享队列中的urls
        :param db_name: 数据库的名字
        :param collection_name: 表的名字
        :return:
        """
        db = self.__client[db_name]
        db.drop_collection(collection_name)
        db[collection_name].insert_many([{'url': crawl_url} for crawl_url in crawl_urls])

    @deal_exceptions(print_exceptions=False)
    def save_html_data(self, data, db_name='blockchain_data',
                       collection_name='html_data', is_append=False):
        """
        将爬取到的html数据存储到MongoDB中
        :param db_name: mongoDB数据库名称
        :param data: 需要存储的数据
        :param collection_name: collect名称（概念类似SQL的表）
        :param is_append: 是否以追加的形式插入数据库(default=False)
        :return: True || False
        """
        if data:
            if is_append:
                self.__client[db_name][collection_name].update({'source_url': data['source_url']},
                                                               {'$set': data}, True)
            else:
                self.__client[db_name][collection_name].insert_one(data)
