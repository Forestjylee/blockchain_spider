# -*- coding: utf-8 -*-
"""

@file: __init__.py.py
@time: 2018/10/22 10:49
Created by Junyi.
"""
from settings import (
    MONGODB_HOST,
    MONGODB_PORT,
    MONGODB_DATABASE_NAME,
    MONGODB_COLLECTION_NAME,
)
from .mongo_pipline import MongoPipline
from .normal_pipline import NormalPipline


def get_pipline_object(pipline_type):
    """
    获取共享url队列对象
    :param pipline_type:采用队列的类型
    :return: ->queue object
    """
    if pipline_type == "MongoDB":
        return MongoPipline(
            host=MONGODB_HOST,
            port=MONGODB_PORT,
            db_name=MONGODB_DATABASE_NAME,
            collection_name=MONGODB_COLLECTION_NAME,
        )
    elif pipline_type == "normal":
        return NormalPipline()
    else:
        print(f"{pipline_type} is not support!")
        exit(-1)
