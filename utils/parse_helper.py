# -*- coding: utf-8 -*-
"""
parse部分
@file: parse_helper.py
@time: 2018/10/31 19:59
Created by Junyi.
"""
from datetime import datetime
from pipline.mongo_pipline import MongoPipline


class ParseHelper(object):

    mongo_tube = MongoPipline()

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
        if response and response.status_code == 200 and cls.__is_text_html(response):
            absolute_links, text = response.html.absolute_links, response.html.text
            data = {
                        'source_url': response.url,
                        'urls': absolute_links,
                        'text': text,
                        'datetime': str(datetime.now()),
            }
            cls.mongo_tube.save_html_data_to_mongo(data)
            return data
        else:
            return None

    @staticmethod
    def __is_text_html(response):
        """
        判断网页是否为text/html格式的
        :param response: 网页的响应
        :return: True | False
        """
        try:
            content_type = response.headers['Content_Type']
            if content_type == 'text/html':
                return True
            else:
                return False
        except:
            return False
