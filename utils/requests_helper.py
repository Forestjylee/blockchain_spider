# -*- coding: utf-8 -*-
"""
发起HTTP  GET请求并接收返回结果
@file: get_helper.py
@time: 2018/10/25 19:20
Created by Junyi.
"""
from requests_html import HTMLSession


def request_url(url):
    """
    发起get请求得到网页响应
    :param url: 目标网页url
    :return: ->response(Request.response)
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    sess = HTMLSession()
    try:
        response = sess.get(url, headers)
    except:
        response = None
    return response
