# -*- coding: utf-8 -*-
"""
url_queue模块单元测试
@file: test_url_queue.py
@time: 2018/12/2 21:54
Created by Junyi.
"""
from url_queue.redis_queue import RedisQueue


class TestURLQueue(object):

    def test_connection(self):
        self.redis_queue = RedisQueue(host='localhost', queue_name='test_queue')

    def test_put_url_in_queue(self):
        self.redis_queue = RedisQueue(host='localhost', queue_name='test_queue')
        self.redis_queue.put_url_in_queue(item='https://www.baidu.com')

    def test_get_queue_length(self):
        self.redis_queue = RedisQueue(host='localhost', queue_name='test_queue')
        print(f"当前列表长度为{self.redis_queue.get_queue_len()}")

    def test_get_url_from_queue(self):
        self.redis_queue = RedisQueue(host='localhost', queue_name='test_queue')
        print(f"列表中的{self.redis_queue.get_url_from_queue()}被弹出")

    def test_delete_queue(self):
        self.redis_queue = RedisQueue(host='localhost', queue_name='test_queue')
        self.redis_queue.delete_queue()
