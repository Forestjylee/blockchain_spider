# -*- coding: utf-8 -*-
"""
工具装饰器
@file: decorator.py
@time: 2018/10/31 20:59
Created by Junyi.
"""
import time
from requests import get
from .io_helper import save_as_json, save_as_pickle


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


def with_log(logger, message):
    """
    日志装饰器
    :param logger: logger object
    :param message: 需要输出的信息
    :return: None
    """
    def swapper(func):
        def _swapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            logger.info(message)
            return ret
        return _swapper
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
            save_as_pickle(data, file_path, print_result)
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
            save_as_json(data, file_path, print_result)
            return data
        return _swapper
    return swapper


def deal_exceptions(print_exceptions=False):
    """
    不关心函数的返回结果
    执行成功则返回
    执行失败则返回None
    :param print_exceptions: 是否将错误信息打印到控制台(default=False)
    :return: True | False
    """
    def _swapper(func):
        def swapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if print_exceptions:
                    print(repr(e))
                return None
        return swapper
    return _swapper


def ensure_network_env(func):
    """
    在运行函数之前，判断网络环境是否正常
    异常则抛出ConnectionError错误
    :return: ->func's return | Exceptions
    """
    def swapper(*args, **kwargs):
        try:
            get('http://www.baidu.com')
            return func(*args, **kwargs)
        except:
            raise ConnectionError("当前网络环境异常!")
    return swapper