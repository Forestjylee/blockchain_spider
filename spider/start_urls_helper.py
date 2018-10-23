# -*- coding: utf-8 -*-
"""
start_urls.py的辅助函数
@file: start_urls_helper.py
@time: 2018/10/23 18:48
Created by Junyi.
"""


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
                starts_urls.append(search_result)
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


def _get_baidu_next_page_url(html):
    """
    获取百度搜索下一页结果的url
    :param html: response.html(Type "HTML")
    :return: next_page_url
    """
    try:
        refer_link = html.find('a', containing='下一页')[-1].attrs['href']
        next_page_url = f"https://www.baidu.com{refer_link}"
    except TypeError:
        next_page_url = None
    return next_page_url


def _get_sogou_next_page_url(html):
    """
    获取搜狗搜索下一页结果的url
    :param html: response.html(Type "HTML")
    :return: next_page_url
    """
    try:
        refer_link = html.find('#sogou_next')[0].attrs['href']
        next_page_url = f"https://www.sogou.com/web{refer_link}"
    except TypeError:
        next_page_url = None
    return next_page_url


def _get_bing_next_page_url(html):
    """
    获取必应搜索下一页结果的url
    :param html: response.html(Type "HTML")
    :return: next_page_url
    """
    try:
        refer_link = html.search('title=\"下一页\" href=\"{}\"')[0].replace('amp;', '')
        next_page_url = f"https://cn.bing.com{refer_link}"
    except TypeError:
        next_page_url = None
    return next_page_url
