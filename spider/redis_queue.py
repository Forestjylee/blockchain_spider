# -*- coding: utf-8 -*-
"""
使用redis实现共享url队列
@file: redis_queue.py
@time: 2018/10/31 14:51
Created by Junyi.
"""
import redis


class RedisQueue(object):

    def __init__(self, host='localhost', queue_name='blockchain_urls'):
        """
        初始化redis队列对象
        :param host: redis的ip
        :param queue_name: 队列的名称
        """
        self.host = host
        self.queue_name = queue_name
        self.redis_queue = self.__get_redis_queue()

    def __get_redis_queue(self):
        """
        获取redis队列对象
        :return: ->redis_queue
        """
        redis_queue = redis.Redis(host=self.host, port=6379)
        return redis_queue

    def get_queue_len(self):
        """
        获取共享url队列的长度
        :return: ->length of queue<int>
        """
        return self.redis_queue.llen(self.queue_name)

    def get_url_from_queue(self):
        """
        取出redis队列第一个元素
        :return: ->item | None(队列为空时)
        """
        return self.redis_queue.lpop()

    def put_url_in_queue(self, item):
        """
        将item压入redis队列中
        :param item: 需要push的元素
        :return: 队列当前长度
        """
        return self.redis_queue.rpush(self.queue_name, item)

    def put_urls_in_queue(self, items):
        """
        将多个items压进队列
        :param items: 需要push的元素
        :return: 队列当前长度
        """
        for item in items:
            yield self.redis_queue.rpush(self.queue_name, item)
