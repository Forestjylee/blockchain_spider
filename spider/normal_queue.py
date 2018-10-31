# -*- coding: utf-8 -*-
"""
采用multiprocess.Manager的队列对象实现队列
@file: normal_queue.py
@time: 2018/10/31 15:56
Created by Junyi.
"""
from multiprocessing import Manager


class NormalQueue(object):

    def __init__(self):
        manager = Manager()
        self.lock = manager.Lock()
        self.queue = manager.Queue()

    def get_queue_len(self):
        """
        获取队列长度
        :return: ->queue_len<int>
        """
        return self.queue.qsize()

    def put_url_in_queue(self, item):
        """
        将一个item压入队列尾部
        :param item: 需要push的元素
        :return: None
        """
        self.lock.acquire()
        self.queue.put(item)
        self.lock.release()

    def put_urls_in_queue(self, items):
        """
        将多个items压入队列尾部
        :param items: 需要push的多个元素
        :return: None
        """
        for item in items:
            self.put_url_in_queue(item)

    def get_url_from_queue(self):
        """
        取出队列第一个元素
        :return: ->item | None(队列为空时)
        """
        if not self.queue.empty():
            return self.queue.get()
        else:
            return None
