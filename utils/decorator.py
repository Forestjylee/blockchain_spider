# -*- coding: utf-8 -*-
"""
工具装饰器
@file: decorator.py
@time: 2018/10/31 20:59
Created by Junyi.
"""
import time
from pipline.normal_pipline import NormalPipline


def timeit(func):
    """
    测试函数运行消耗时间的装饰器
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @timeit
    def test(a, b):
        i = b - a
        for i in range(100090):
            i += 1
        return i
    Console print: function test() running cost 0.004984617233276367 secs.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :param func: 需要测试运行时间的函数
    :return: ->func's return and print cost time
    """
    def swapper(*args, **kwargs):
        time1 = time.time()
        func_ret = func(*args, **kwargs)
        print(f"function {func.__name__}() running cost {time.time() - time1} secs.")
        return func_ret
    return swapper


def to_pickle(file_path, print_result=True):
    """
    将函数返回结果自动序列化并存储的装饰器
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @to_pickle('C:\\', True)
    def test():
        return {
            'a': 1,
            'b': 2,
        }
    Console print: Save as pickle success!
    [And a pickled file will generate in the file_path you give]
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :param file_path: 文件保存路径
    :param print_result: 是否将保存结果输出到屏幕
    :return: func's return
    """
    def swapper(func):
        def _swapper(*args, **kwargs):
            data = func(*args, **kwargs)
            NormalPipline.save_as_pickle(data, file_path, print_result)
            return data
        return _swapper
    return swapper


def to_json(file_path, print_result=True):
    """
    将函数返回结果自动json格式化并存储的装饰器
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @to_json('C:\\', True)
    def test():
        return {
            'a': 3,
            'b': 4,
        }
    Console print: Save as json success!
    [And a json file will generate in the file_path you give]
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :param file_path: 文件保存路径
    :param print_result: 是否将保存结果输出到屏幕
    :return: func's return
    """
    def swapper(func):
        def _swapper(*args, **kwargs):
            data = func(*args, **kwargs)
            NormalPipline.save_as_json(data, file_path, print_result)
            return data
        return _swapper
    return swapper
