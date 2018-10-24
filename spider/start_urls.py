# -*- coding: utf-8 -*-
"""
爬虫的起始url
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
e.g.: start_urls = get_start_urls('baidu', '区块链', 30)
Get 30 start_urls about '区块链' from baidu.
备注：bing网站存在一定反爬措施，使得多次请求无法得到结果
     实际操作中尽量不要过多使用bing进行搜索。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@file: start_urls.py
@time: 2018/10/22 10:53
Created by Junyi.
"""
from .start_urls_helper import (parse_baidu_response, parse_sogou_response,
                                parse_bing_response, get_target_start_urls)

BAIDU_URL_TEMPLATE = "https://www.baidu.com/s?ie=UTF-8&wd={}"

SOGOU_URL_TEMPLATE = "https://www.sogou.com/web?query={}"

BING_URL_TEMPLATE = "https://cn.bing.com/search?q={}"


def get_baidu_start_urls(keyword, amount):
    """
    通过百度的搜索结果，获取起始地址池
    :param keyword: 关键词
    :param amount；需要起始url的数量
    :return: ->start_urls(list)
    """
    start_urls = get_target_start_urls(BAIDU_URL_TEMPLATE, keyword,
                                       parse_baidu_response, amount)
    return start_urls


def get_sogou_start_urls(keyword, amount):
    """
    通过搜狗的搜索结果，获取起始地址池
    :param keyword: 关键词
    :param amount: 需要起始url的数量
    :return: ->start_urls(list)
    """
    start_urls = get_target_start_urls(SOGOU_URL_TEMPLATE, keyword,
                                       parse_sogou_response, amount)
    return start_urls


def get_bing_start_urls(keyword, amount):
    """
    通过必应国内版的搜索结果，获取起始地址池
    :param keyword: 关键词
    :param amount: 需要起始url的数量
    :return: ->start_urls(list)
    """
    start_urls = get_target_start_urls(BING_URL_TEMPLATE, keyword,
                                       parse_bing_response, amount)
    return start_urls


def get_start_urls(search_engine, keyword, amount=10):
    """
    顶层封装，供外部调用
    :param search_engine: 使用搜索引擎的类型(baidu, sogou, bing)
    :param keyword: 搜索关键字
    :param amount: 需要起始url的数量(默认为10)
    :return: ->start_urls(list)
    """
    if search_engine == 'baidu':
        return get_baidu_start_urls(keyword, amount)
    elif search_engine == 'sogou':
        return get_sogou_start_urls(keyword, amount)
    elif search_engine == 'bing':
        return get_bing_start_urls(keyword, amount)
    else:
        raise AttributeError
