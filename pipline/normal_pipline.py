# -*- coding: utf-8 -*-
"""
使用pickle,json等常规手段序列保存到磁盘上
@file: normal_pipline.py
@time: 2018/10/31 20:34
Created by Junyi.
"""
import pickle
import json
# TODO [需要重写]API封装要与Mongo_pipline统一


class NormalPipline(object):
    """
    对pickle序列化和json格式化进行封装
    """
    @staticmethod
    def save_as_pickle(data, file_path, print_result=True):
        if data:
            with open(file_path, 'wb') as fw:
                pickle.dump(data, fw)
            if print_result:
                print(f"Save to {file_path} as pickle success!")
        else:
            print(f"{data.__name__} which going to save is None.")

    @staticmethod
    def read_pickle_file(file_path):
        with open(file_path, 'rb') as fr:
            return pickle.load(fr)

    @staticmethod
    def append_as_pickle(data, file_path, print_result=True):
        old_data = NormalPipline.read_pickle_file(file_path)
        if isinstance(old_data, (list, dict)):
            data = old_data.append(data)
            NormalPipline.save_as_pickle(data, file_path, print_result)
            if print_result:
                print(f"Append to {file_path} as pickle success!")
        else:
            raise TypeError("原本的数据必须是列表或字典才可以追加")

    @staticmethod
    def save_as_json(data, file_path, print_result=True):
        if data:
            with open(file_path, 'w') as fw:
                json.dump(data, fw, ensure_ascii=False)
            if print_result:
                print(f"Save to {file_path} as json success!")
        else:
            print(f"{data.__name__} which going to save is None.")

    @staticmethod
    def read_json_file(file_path):
        with open(file_path, 'r') as fr:
            return json.load(fr)

    @staticmethod
    def append_as_json(data, file_path, print_result=True):
        old_data = NormalPipline.read_json_file(file_path)
        if isinstance(old_data, (list, dict)):
            data = old_data.append(data)
            NormalPipline.save_as_json(data, file_path, print_result)
            if print_result:
                print(f"Save to {file_path} as json success!")
        else:
            raise TypeError("原本的数据必须是列表或字典才可以追加")
