# blockchain_spider

✨区块链爬虫项目✨

## 1.项目文件目录

│  Pipfile
│  Pipfile.lock
│  run_spider.py
│
├─pipline
│  │  mongo_pipline.py
│  │  normal_pipline.py
│  │  __init__.py
│ 
├─spider
│  │  multiprocess_spider.py
│  │  start_urls_spider.py
│  │  __init__.py
│
├─url_queue
│  │  normal_queue.py
│  │  redis_queue.py
│  │  __init__.py
│
└─utils
    │  decorator.py
    │  log_helper.py
    │  parse_helper.py
    │  requests_helper.py
    │  start_urls_helper.py
    │  __init__.py





## 2.开发环境

##### 操作系统：Windows 10(64bit)

##### python解释器：CPython 3.7.1

##### 包管理工具：Pipenv  (version 2018.10.13)

##### IDE集成开发环境：PyCharm 2018.2





## 3.怎么使用blockchain_spider

### 3.1.准备运行环境

##### 创建blockchain_spider运行的虚拟环境：

```python
cd blockchain_spider
pipenv install
```

##### 若提示找不到pipenv命令，请检查环境变量是否配置正确然后安装pipenv，命令：

```python
pip install pipenv
```

##### （需要注意的是，blockchain_spider的运行环境是python3.7，请确保本地存在python3.7解释器）



### 3.2准备数据库环境

##### 若使用高性能版本的blockchain_spider,则需配置MongoDB数据库，以及Redis数据库

##### 由于MongoDB数据库和Redis数据库的安装过程比较简单清晰，此处不再赘述

##### (1)MongoDB安装完成之后，运行在默认端口(port:27017)即可

##### Windows环境下将MongoDB在配置成系统服务，打开cmd：

```

```

##### 开启配置好的系统服务，无异常则说明MongoDB数据库正常运行

##### (2)Redis同样运行在默认端口(port:6379)

##### Windows环境下开启Redis数据库，打开cmd：

```
cd redis(进入redis安装目录)
start redis-server.exe
```

##### 回车之后会弹出一个新的cmd窗口，没有异常则表示redis成功运行



### 3.3运行爬虫

##### （高性能版本）在blockchain_spider文件夹中打开cmd,输入：

```python
pipenv run run_spider.py
```

##### （展示版本）在blockchain_spider文件夹中打开cmd，输入：

```
pipenv run run_test_spider.py
```



