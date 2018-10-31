# -*- coding: utf-8 -*-
"""
与数据库的交互部分
@file: data_handler.py
@time: 2018/10/25 19:42
Created by Junyi.
"""
import pymongo


def get_mongo_database(db_name):
    """
    获取操作mongoDB数据库的对象
    :param db_name: 数据库名称
    :return: db Object
    """
    client = pymongo.MongoClient('localhost')
    db = client[db_name]
    return db


def get_crawl_urls():
    """"""
    client = pymongo.MongoClient('localhost')
    db = client['crawl_urls']
    #TODO 从数据库中提取信息
    pass


def save_html_data_to_mongo(db, data):
    """
    将爬取到的html数据存储到MongoDB中
    :param db: mongoDB数据库对象
    :param data: 需要存储的数据
    :return: True || False
    """
    if db['html_data'].update({'source_url': data['source_url']}, {'$set': data}, True):
        #TODO logging记录日志
        return True
    else:
        return False