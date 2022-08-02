# -*- coding: utf-8 -*-
"""
@date: 2022-7-15
@author: luhx
@funcs: 文件相关操作
"""
import os
import re
from typing import List


def valid_contract_file(file_name) -> bool:
    """文件是形如下面的谁的名：SH#600981.txt，SZ#301024.txt，返回True,否则返回False"""
    result = re.match('SZ|SH#\d{6}.txt', file_name)
    # result = re.match('rb\d{2,4}\.csv', file_name)
    return result is not None


def get_file_list(path, funcs=None) -> List[str]:
    """
    返回文件夹下的文件列表
    """
    file_path_list = []
    name_list = []
    files = os.listdir(path)
    for file in files:
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            continue
        else:
            if funcs is None:
                file_path_list.append(cur_path)
                name_list.append(file)

            elif funcs(file):
                file_path_list.append(cur_path)
                name_list.append(file)
    return name_list


def read_lines(path_file, head=False)->List[str]:
    """
    按行读取数据,返回字符串数组
    head为真时，第1行认为是表头，过滤
    """
    lines = list()
    with open(path_file, encoding='gb2312', mode='r') as f:
        if head:
            f.readline()
        while True:
            line = f.readline()
            if line:
                lines.append(line)
            else:
                break
    return lines


if __name__ == '__main__':
    files = get_file_list(r"E:\work\data\FutAC_Min1_Std_202112", valid_contract_file)
    if files:
        lines = read_lines(files[0])
        [print(txt) for txt in lines]