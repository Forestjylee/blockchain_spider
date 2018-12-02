# -*- coding: utf-8 -*-
"""

@file: __init__.py.py
@time: 2018/10/31 20:27
Created by Junyi.
"""
from settings import REDIS_HOST, URL_QUEUE_NAME
from .redis_queue import RedisQueue
from .normal_queue import NormalQueue


def get_queue_object(queue_type):
    """
    获取共享url队列对象
    :param queue_type:采用队列的类型
    :return: ->queue object
    """
    if queue_type == 'redis':
        return RedisQueue(REDIS_HOST, URL_QUEUE_NAME)
    elif queue_type == 'normal':
        return NormalQueue()
    else:
        print(f"{queue_type} is not support!")
        exit(-1)
