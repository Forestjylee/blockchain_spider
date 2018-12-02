# -*- coding: utf-8 -*-
"""
parse部分
@file: parse_helper.py
@time: 2018/10/31 19:59
Created by Junyi.
"""
from datetime import datetime


class ParseHelper(object):

    @classmethod
    def first_parse_response(cls, response, keyword):
        """
        初步解析response
        :param response: 网页返回的response
        :param keyword: 检索关键字
        :return: {
                    'source_url': 网站的网址,
                    'urls': 网页中所有链接,
                    'text': 网页中的所有文本,
                    'datetime': datetime,
        } | None
        """
        if response:
            html = response.html
            text = html.text
            if cls.is_include_keyword(text, keyword):
                data = {
                    "source_url": response.url,
                    "urls": list(html.absolute_links),
                    "text": text,
                    "datetime": str(datetime.now()),
                }
                return data
            else:
                return None
        else:
            return None

    @staticmethod
    def is_include_keyword(text, keyword):
        """
        获取到的网页文本是否包含关键字
        防止爬虫跑偏
        :param text: 网页文本
        :param keyword: 关键字
        :return: -> True | False
        """
        if keyword in text:
            return True
        else:
            return False
