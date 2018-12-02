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

    def __init__(self, host, port, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
        self.__client = pymongo.MongoClient(host=host, port=port)

    @deal_exceptions(print_exceptions=False)
    def save_html_data(
        self,
        data,
        is_append=False,
    ):
        """
        将爬取到的html数据存储到MongoDB中
        :param data: 需要存储的数据
        :param is_append: 是否以追加的形式插入数据库(default=False)
        :return: True || False
        """
        if data:
            if is_append:
                self.__client[self.db_name][self.collection_name].update(
                    {"source_url": data["source_url"]}, {"$set": data}, True
                )
            else:
                self.__client[self.db_name][self.collection_name].insert_one(data)
