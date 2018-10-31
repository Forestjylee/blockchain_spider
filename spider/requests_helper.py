# -*- coding: utf-8 -*-
"""
发起HTTP  GET请求并接收返回结果
@file: get_helper.py
@time: 2018/10/25 19:20
Created by Junyi.
"""
from datetime import datetime
from requests_html import HTMLSession
from .data_handler import save_html_data_to_mongo

#TODO 日志记录模块


def request_url(url):
    """
    发起get请求得到网页响应
    :param url: 目标网页url
    :return: ->response(Request.response)
    """
    sess = HTMLSession()
    try:
        response = sess.get(url)
    except:
        response = None
    return response


def first_parse_response(response):
    """
    初步解析response

    :param response: 网页返回的response
    :return: {'urls': 网页中所有链接, 'text':网页中的所有文本
              'datetime':datetime} | None
    """
    if response and response.status_code == 200:
        absolute_links, text = response.html.absolute_links, response.html.text
        data = {
                    'source_url': response.url,
                    'urls': absolute_links,
                    'text': text,
                    'datetime': str(datetime.now())}
        save_html_data_to_mongo(data)
        return data
    else:
        return None
