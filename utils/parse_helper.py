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
    def first_parse_response(cls, response):
        """
        初步解析response
        :param response: 网页返回的response
        :return: {
                    'source_url': 网站的网址,
                    'urls': 网页中所有链接,
                    'text': 网页中的所有文本,
                    'datetime': datetime,
        } | None
        """
        if response:
            html = response.html
            data = {
                        'source_url': response.url,
                        'urls': list(html.absolute_links),
                        'text': html.text,
                        'datetime': str(datetime.now()),
            }
            return data
        else:
            return None
