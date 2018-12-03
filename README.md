# blockchain_spider🕷

✨**区块链爬虫项目**✨

**Github:** 🌏https://github.com/Forest75/blockchain_spider

## 1.项目文件目录

```powershell

```





## 2.开发环境

##### 操作系统：Windows 10(64bit)

##### python解释器：CPython 3.7.1

##### 包管理工具：Pipenv  (version 2018.10.13)

##### IDE集成开发环境：PyCharm 2018.2





## 3.怎么使用blockchain_spider

### 3.0查看外部依赖

##### 在blockchain_spider目录下打开cmd，输入：

```python
>>> pipenv graph
>>>
coverage==4.5.2
pymongo==3.7.2
redis==2.10.6
requests-html==0.9.0
  - bs4 [required: Any, installed: 0.0.1]
    - beautifulsoup4 [required: Any, installed: 4.6.3]
  - fake-useragent [required: Any, installed: 0.1.11]
  - parse [required: Any, installed: 1.9.0]
  - pyppeteer [required: >=0.0.14, installed: 0.0.25]
    - appdirs [required: Any, installed: 1.4.3]
    - pyee [required: Any, installed: 5.0.0]
    - tqdm [required: Any, installed: 4.28.1]
    - urllib3 [required: Any, installed: 1.24]
    - websockets [required: Any, installed: 6.0]
  - pyquery [required: Any, installed: 1.4.0]
    - cssselect [required: >0.7.9, installed: 1.0.3]
    - lxml [required: >=2.1, installed: 4.2.5]
  - requests [required: Any, installed: 2.20.0]
    - certifi [required: >=2017.4.17, installed: 2018.10.15]
    - chardet [required: >=3.0.2,<3.1.0, installed: 3.0.4]
    - idna [required: >=2.5,<2.8, installed: 2.7]
    - urllib3 [required: >=1.21.1,<1.25, installed: 1.24]
  - w3lib [required: Any, installed: 1.19.0]
    - six [required: >=1.4.1, installed: 1.11.0]
pytest==4.0.1
  - atomicwrites [required: >=1.0, installed: 1.2.1]
  - attrs [required: >=17.4.0, installed: 18.2.0]
  - colorama [required: Any, installed: 0.4.1]
  - more-itertools [required: >=4.0.0, installed: 4.3.0]
    - six [required: >=1.0.0,<2.0.0, installed: 1.11.0]
  - pluggy [required: >=0.7, installed: 0.8.0]
  - py [required: >=1.5.0, installed: 1.7.0]
  - setuptools [required: Any, installed: 40.4.3]
  - six [required: >=1.10.0, installed: 1.11.0]
```

##### [↑↑↑上面输出的是v0.1版本的外部依赖信息↑↑↑]

##### 若提示找不到pipenv命令，请检查环境变量是否配置正确然后安装pipenv，命令：

```python
>>> pip install pipenv
```

##### （需要注意的是，blockchain_spider的运行环境是python3.7，请确保本地存在python3.7解释器）

### 3.1准备运行环境

##### 创建blockchain_spider运行的虚拟环境：

```python
>>> cd blockchain_spider
>>> pipenv install
```



### 3.2准备数据库环境

##### 若使用高性能版本的blockchain_spider,则需配置MongoDB数据库，以及Redis数据库

##### 由于MongoDB数据库和Redis数据库的安装过程比较简单清晰，此处不再赘述

##### (1)MongoDB安装完成之后，运行在默认端口(port:27017)即可

##### 打开cmd，输入：

```python
>>> cd mongo/3.4/bin
>>> mongod --dbpath [此处输入希望数据保存的文件夹绝对路径]
```

##### 无异常则说明MongoDB数据库正常运行

##### (2)Redis同样运行在默认端口(port:6379)

##### Windows环境下开启Redis数据库，打开cmd：

```python
>>> cd redis(进入redis安装目录)
>>> start redis-server.exe
```

##### 回车之后会弹出一个新的cmd窗口，没有异常则表示redis成功运行



### 3.3运行爬虫

##### 打开cmd控制台，激活虚拟环境：

```python
>>> cd blockchain_spider
>>> pipenv shell
```

##### 在settings.py中配置好之后，输入以下命令运行爬虫：

```python
(blockchain_spider)>>> python run_spider.py
```

##### 或者可以在其他地方通过导入blockchain_spider包来运行,新建一个run.py文件：

```python
# @file: run.py
from blockchain_spider import spider_run


if __name__ == '__main__':
    spider_run()
```


```python
>>> python run.py
```





## 4.运行过程

### 4.1控制台输出

##### 每成功爬取一个url，就在控制台中输出：

```powershell
[2018/11/01 5:01:00 PM] INFO: URL is crawled.
[2018/11/01 5:01:01 PM] INFO: There are XXX urls in queue now.
```



### 4.2运行日志

##### 会自动在运行目录下生成2个日志文件

```diff
./2018-XX-XX-spider.log
./2018-XX-XX-requests.log
```

##### 分别记录了爬取url的情况和http请求的情况



### 4.3数据库

#### 4.3.1MongoDB

##### MongoDB用于存储爬取到的text文本信息

##### 数据存放在blockchain_data数据库的html_data表中：

##### 单条数据格式为

```python
data = {
        'source_url': 来源URL,
        'urls': 指向外部的URL,
        'text': 网页中的text文本,
        'datetime': 存储的时间[XXXX-XX-XX XX:XX:XX],
}
```

#### 4.3.2Redis

##### Redis用于作为共享url队列，协调多个爬虫之间的请求调度

##### 运行过程中url会不停进出队列，出现意外情况url也不会丢失，而是保存在队列中等待下次运行





## 5.可以进一步改进的地方

##### （下列内容针对高性能爬虫部分）

### 5.1请求部分与后续处理部分未分离

#####         在blockchain_spider（v0.1）的实现过程中，由于时间关系，将request部分和parse部分合并到同一个进程中执行。虽然parse部分并没有使用选择器进行筛选，但是依旧会有一点点时间开销，加上读写数据库和输出日志的时间，会使整体的运行效率有所下降。

#### 建议优化方案：

##### （1）创建一个response队列，专门用于存储request部分接收到的返回值

##### （2）parse部分和后续处理部分从response队列中不断取出response进行操作(多进程实现)

##### （3）request部分只负责发起HTTP请求(多线程实现)并将结果存入response队列



### 5.2日志记录不够完善

#####         blockchain_spider（v0.1）的只记录了请求日志和最终结果日志，中间处理过程的日志并没有记录。没有实现的原因是代码会因为加入日志记录而变得十分冗余，后续视情况添加详细的日志记录。



### 5.3异常处理不够精细

#####        考虑到爬取的数据量会比较大，所以遇到异常情况采取直接舍弃该url的策略。对于一般情况而言，这可能不会有什么问题，但是也存在丢失一部分关键信息的可能性。

