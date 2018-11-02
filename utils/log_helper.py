# -*- coding: utf-8 -*-
"""
日志模块
@file: log_helper.py
@time: 2018/10/31 21:53
Created by Junyi.
"""
import logging
from datetime import date


def get_logger(logger_name='MyLogger', level=logging.INFO,
               to_console=True, to_file=False, filename=None):
    """
    获取一个logger
    :param logger_name: logger的名称
    :param level: 过滤等级
    :param to_console: 是否输出到控制台(default=True)
    :param to_file:  是否输出到文件(default=False)
    :param filename: 日志文件名
    :return: logger object
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    if to_console:
        logger.addHandler(get_log_handler(handler_object=logging.StreamHandler, level=level))
    if to_file:
        logger.addHandler(get_log_handler(handler_object=logging.FileHandler, level=level,
                                          file_name=filename))
    return logger


def get_log_handler(handler_object, file_name=None, level=logging.INFO):
    """
    获取一个log handler
    常用的有StreamHandler和FileHandler
    分别用于输出控制台日志和文件日志
    :param level: 过滤等级
    :param file_name: 保存日志的文件名
    :param handler_object: handler object
    :return: logger object with new handler.
    """
    log_handler = handler_object(filename=get_file_name(file_name)) if file_name else handler_object()
    log_handler.setLevel(level)
    log_format = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s',
                                    datefmt='%Y/%m/%d %I:%M:%S %p')
    log_handler.setFormatter(log_format)
    return log_handler


def get_file_name(keyword='spider'):
    """
    根据当前日期自动生成一个文件名
    :param keyword: 自动生成文件名的关键字
    :return: file_name
    """
    now_date = date.today()
    file_name = f"{str(now_date)}-{keyword}.log"
    return file_name
