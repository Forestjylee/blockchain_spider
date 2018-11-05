# -*- coding: utf-8 -*-
"""

@file: __init__.py.py
@time: 2018/10/22 10:49
Created by Junyi.
"""
from .mongo_pipline import MongoPipline
from .normal_pipline import NormalPipline


def get_pipline_object(pipline_type):
    """
    获取共享url队列对象
    :param pipline_type:采用队列的类型
    :return: ->queue object
    """
    if pipline_type == 'mongo':
        return MongoPipline()
    elif pipline_type == 'normal':
        return NormalPipline()
    else:
        raise TypeError(f"{pipline_type} is not support!")