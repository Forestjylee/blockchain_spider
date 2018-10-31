# -*- coding: utf-8 -*-
"""
使用pickle,json等常规手段序列保存到磁盘上
@file: normal_pipline.py
@time: 2018/10/31 20:34
Created by Junyi.
"""
import pickle
import json


class NormalPipline(object):
    """
    对pickle序列化和json格式化进行封装
    """
    @staticmethod
    def save_as_pickle(data, file_path, print_result=True):
        with open(file_path, 'wb') as fw:
            pickle.dump(data, fw)
        if print_result:
            print("Save as pickle success!")

    @staticmethod
    def read_pickle_file(file_path):
        with open(file_path, 'rb') as fr:
            data = pickle.load(fr)
        return data

    @staticmethod
    def append_as_pickle(data, file_path, print_result=True):
        old_data = NormalPipline.read_pickle_file(file_path)
        if isinstance(old_data, (list, dict)):
            data = old_data.append(data)
            NormalPipline.save_as_pickle(data, file_path, print_result)
        else:
            raise TypeError("原本的数据必须是列表或字典才可以追加")

    @staticmethod
    def save_as_json(data, file_path, print_result=True):
        with open(file_path, 'w') as fw:
            json.dump(data, fw, ensure_ascii=False)
        if print_result:
            print("Save as json success!")

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
        else:
            raise TypeError("原本的数据必须是列表或字典才可以追加")
