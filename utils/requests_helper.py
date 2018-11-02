# -*- coding: utf-8 -*-
"""
发起HTTP  GET请求并接收返回结果
@file: get_helper.py
@time: 2018/10/25 19:20
Created by Junyi.
"""
from requests_html import HTMLSession
from utils.log_helper import get_logger
from utils.decorator import deal_exceptions

requests_logger = get_logger(logger_name='requests_logger', to_console=False,
                             to_file=True, filename='requests')


def is_useful_response(func):
    """
    判断response是否为文本型html的装饰器
    :param func: 需要装饰的函数
    :return: response | None
    """
    def swapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code == 200:
            content_type = response.headers['Content-Type']
            if 'text/html' in content_type:
                requests_logger.info(f"Request {response.url} successful!")
            else:
                requests_logger.warning(f"{response.url} is not a text html page!")
                response = None
            return response
        else:
            requests_logger.warning(f"{response.url}'s status_code is not 200!")
            return None
    return swapper


@deal_exceptions(print_exceptions=False)
@is_useful_response
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
    session = HTMLSession()
    response = session.get(url, headers=headers)
    return response
