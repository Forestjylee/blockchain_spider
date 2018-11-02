# -*- coding: utf-8 -*-
"""
start_urls.py的辅助函数
@file: start_urls_helper.py
@time: 2018/10/23 18:48
Created by Junyi.
"""
from requests_html import HTMLSession
from .decorator import deal_exceptions


def parse_baidu_response(response):
    """
    解析百度搜索结果页面
    :param response: 网页的响应
    :return: ->start_urls(list), ->next_page_url(str)
    """
    starts_urls = []
    next_page_url = None
    if response.status_code == 200:
        html = response.html
        search_results_list = html.absolute_links
        for search_result in search_results_list:
            if 'http://www.baidu.com/link?url=' in search_result:
                starts_urls.append(search_result)
        next_page_url = _get_baidu_next_page_url(html)
    return starts_urls, next_page_url


def parse_sogou_response(response):
    """
    解析搜狗搜索结果页面
    :param response: 网页的响应
    :return: ->start_urls(list), ->next_page_url(str)
    """
    starts_urls = []
    next_page_url = None
    if response.status_code == 200:
        html = response.html
        search_results_list = html.absolute_links
        for search_result in search_results_list:
            if 'https://www.sogou.com/link?url=' in search_result:
                real_url = _get_sogou_real_url(search_result)
                starts_urls.append(real_url)
        next_page_url = _get_sogou_next_page_url(html)
    return starts_urls, next_page_url


def parse_bing_response(response):
    """
    解析必应搜索结果页面
    :param response: 网页的响应
    :return: ->start_urls(list), ->next_page_url(str)
    """
    starts_urls = []
    next_page_url = None
    if response.status_code == 200:
        html = response.html
        search_results_list = html.search_all('target=\"_blank\" href=\"{}\"')
        for search_result in search_results_list:
            starts_urls.append(search_result[0])
        next_page_url = _get_bing_next_page_url(html)
    return starts_urls, next_page_url


@deal_exceptions
def _get_baidu_next_page_url(html):
    """
    获取百度搜索下一页结果的url
    装饰器处理异常，异常情况返回None
    :param html: response.html(Type "HTML")
    :return: next_page_url
    """
    refer_link = html.find('a', containing='下一页')[-1].attrs['href']
    next_page_url = f"https://www.baidu.com{refer_link}"
    return next_page_url


@deal_exceptions
def _get_sogou_next_page_url(html):
    """
    获取搜狗搜索下一页结果的url
    装饰器处理异常，异常情况返回None
    :param html: response.html(Type "HTML")
    :return: next_page_url
    """
    refer_link = html.find('#sogou_next')[0].attrs['href']
    next_page_url = f"https://www.sogou.com/web{refer_link}"
    return next_page_url


@deal_exceptions
def _get_bing_next_page_url(html):
    """
    获取必应搜索下一页结果的url
    装饰器处理异常，异常情况返回None
    :param html: response.html(Type "HTML")
    :return: next_page_url
    """
    refer_link = html.search('title=\"下一页\" href=\"{}\"')[0].replace('amp;', '')
    next_page_url = f"https://cn.bing.com{refer_link}"
    return next_page_url


def _get_sogou_real_url(search_result_url):
    """
    搜狗的搜索结果需要二次请求获取网站真实url
    :param search_result_url: 解析出的直接搜索结果url
    :return: ->real_url(str)
    """
    sess = HTMLSession()
    response = sess.get(search_result_url)
    real_url = response.html.text.split('\"')[1]
    return real_url


def _get_one_page_start_urls(search_url, parse_func, retry_times=0):
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
        _get_one_page_start_urls(search_url, parse_func, retry_times)
    else:
        next_page_url = None
    return start_urls, next_page_url


def get_target_start_urls(url_template, keyword, parse_func, amount):
    """
    获取指定搜索引擎的start_urls
    :param url_template: 指定搜索引擎的url模板
    :param keyword: 搜索关键词
    :param parse_func: 使用的解析函数
    :param amount: 需要的start_urls数量
    :return: ->start_urls(list)
    """
    start_urls = []
    search_url = url_template.format(keyword)
    urls, next_page_url = _get_one_page_start_urls(search_url, parse_func=parse_func)
    if urls:
        start_urls.extend(urls)
    while len(start_urls) < amount and next_page_url:
        urls, next_page_url = _get_one_page_start_urls(next_page_url, parse_func=parse_func)
        if urls:
            start_urls.extend(urls)
    return start_urls
