# -*- coding: utf-8 -*-
"""
pipline模块单元测试
@file: test_pipline.py
@time: 2018/12/2 18:01
Created by Junyi.
"""
from pipline import MongoPipline


class TestMongoPipline(object):
    """MongoDB接口测试类"""

    def test_connection(self):
        """测试能否连接本地MongoDB数据库"""
        self.pipline = MongoPipline(host='localhost', port=27017,
                                    db_name='test', collection_name='pipline_test')

    def test_save_html_data(self):
        """测试能否将数据写入数据库"""
        self.pipline = MongoPipline(host='localhost', port=27017,
                                    db_name='test', collection_name='pipline_test')
        self.pipline.save_html_data(
            data={"test": "测试数据"},
            is_append=False,
        )
