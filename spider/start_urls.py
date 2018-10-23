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
from requests_html import HTMLSession
from .start_urls_helper import (parse_baidu_response, parse_sogou_response,
                                parse_bing_response)

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
    start_urls = []
    search_url = BAIDU_URL_TEMPLATE.format(keyword)
    urls, next_page_url = get_one_page_start_urls(search_url, parse_func=parse_baidu_response)
    while len(start_urls) < amount:
        if urls:
            start_urls.extend(urls)
            if not next_page_url:
                break
            urls, next_page_url = get_one_page_start_urls(next_page_url, parse_func=parse_baidu_response)
        else:
            break
    return start_urls


def get_sogou_start_urls(keyword, amount):
    """
    通过搜狗的搜索结果，获取起始地址池
    :param keyword: 关键词
    :param amount: 需要起始url的数量
    :return: ->start_urls(list)
    """
    start_urls = []
    search_url = SOGOU_URL_TEMPLATE.format(keyword)
    urls, next_page_url = get_one_page_start_urls(search_url, parse_func=parse_sogou_response)
    while len(start_urls) < amount:
        if urls:
            start_urls.extend(urls)
            if not next_page_url:
                break
            urls, next_page_url = get_one_page_start_urls(next_page_url, parse_func=parse_sogou_response)
        else:
            break
    return start_urls


def get_bing_start_urls(keyword, amount):
    """
    通过必应国内版的搜索结果，获取起始地址池
    :param keyword: 关键词
    :param amount: 需要起始url的数量
    :return: ->start_urls(list)
    """
    start_urls = []
    search_url = BING_URL_TEMPLATE.format(keyword)
    urls, next_page_url = get_one_page_start_urls(search_url, parse_func=parse_bing_response)
    while len(start_urls) < amount:
        if urls:
            start_urls.extend(urls)
            if not next_page_url:
                break
            urls, next_page_url = get_one_page_start_urls(next_page_url, parse_func=parse_bing_response)
        else:
            break
    return start_urls


def get_one_page_start_urls(search_url, parse_func, retry_times=0):
    """
    通过一页的搜索结果，获取起始地址
    :param search_url: 关键词
    :param parse_func: 解析函数
    :param retry_times: 特殊情况无法获得请求信息，当前重试次数（设置最大重试次数为5次）
    :return: ->start_urls(list)
    """
    start_urls = []
    session = HTMLSession()
    response = session.get(search_url)
    if response.status_code == 200:
        urls, next_page_url = parse_func(response)
        start_urls.extend(urls)
    elif retry_times <= 5:
        retry_times += 1
        get_one_page_start_urls(search_url, parse_func, retry_times)
    else:
        next_page_url = None
    return start_urls, next_page_url


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
