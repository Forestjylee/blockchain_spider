# -*- coding: utf-8 -*-
"""

@file: io_helper.py
@time: 2018/11/5 17:30
Created by Junyi.
"""
import json
import pickle


def save_as_pickle(data, file_path, print_result=True):
    if data:
        with open(file_path, "wb") as fw:
            pickle.dump(data, fw)
        if print_result:
            print(f"Save to {file_path} as pickle success!")
    else:
        print(f"{data.__name__} which going to save is None.")


def save_as_json(data, file_path, print_result=True):
    if data:
        with open(file_path, "w") as fw:
            json.dump(data, fw, ensure_ascii=False)
        if print_result:
            print(f"Save to {file_path} as json success!")
    else:
        print(f"{data.__name__} which going to save is None.")
