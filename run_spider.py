# -*- coding: utf-8 -*-
"""
项目入口文件
@file: run_spider.py
@time: 2018/11/3 10:15
Created by Junyi.
"""
from spider import run_spider


if __name__ == '__main__':
    try:
        run_spider('区块链', process_num=7, timeout=4)     # 急速模式
        # run_spider('区块链', process_num=4, timeout=4)     # 中速模式
    except Exception as e:
        print(f"Error is {repr(e)}")
