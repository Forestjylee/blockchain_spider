# -*- coding: utf-8 -*-
"""
爬虫的配置文件
@file: settings.py
@time: 2018/12/1 9:50
Created by Junyi.
"""


# 爬取的关键字[必填！！！]
KEYWORD = '区块链'

# 爬虫爬取速度[slow|fast|super_fast]
CRAWL_SPEED = 'super_fast'


########################起始地址池模块##########################

# 来自百度的起始地址数量
BAIDU_START_URLS_AMOUNT = 50

# 来自搜狗的起始地址数量
SOGOU_START_URLS_AMOUNT = 50

# 来自必应的起始地址数量(不稳定，不推荐使用)
BING_START_URLS_AMOUNT = 0

# 百度搜索URL模板
BAIDU_URL_TEMPLATE = "https://www.baidu.com/s?ie=UTF-8&wd={}"

# 搜狗搜索URL模板
SOGOU_URL_TEMPLATE = "https://www.sogou.com/web?query={}"

# 必应搜索URL模板(不稳定)
BING_URL_TEMPLATE = "https://cn.bing.com/search?q={}"

# 爬虫起始地址(url)池的文件路径
START_URLS_SAVE_PATH = 'start_urls.pck'

###############################################################


#########################数据管道模块###########################

# 输送网页数据的管道类型
PIPLINE_TYPE = 'MongoDB'

# MongoDB的主机ip
MONGODB_HOST = 'localhost'

# MongoDB的端口
MONGODB_PORT = 27017

# MongoDB中数据库的名称
MONGODB_DATABASE_NAME = 'blockchain_data'

# MongoDB中数据表的名称
MONGODB_COLLECTION_NAME = 'html_data'

###############################################################


#######################url共享队列模块##########################

# url共享队列的类型
URL_QUEUE_TYPE = 'redis'

# Redis的主机ip
REDIS_HOST = 'localhost'

# Redis中url共享队列的名称
URL_QUEUE_NAME = 'blockchain_urls'

###############################################################


#############################其他##############################

# 并行执行的进程数
PROCESS_NUMBER = 7

# 单次http请求超时时间(/s)
TIMEOUT = 3

# 爬虫日志的文件名
SPIDER_LOG_NAME = 'spider'

# 请求日志的文件名
REQUESTS_LOG_NAME = 'requests'

# 爬取过程中是否忽略一切异常
IGNORE_EXCEPTIONS = True

###############################################################
