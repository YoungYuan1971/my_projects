# -*- coding: UTF-8 -*-
# @time: 2021/3/16 17:28
# @file: 2_pip批量更新库.py
# @Author: YoungYuan

import os

pkg_str = input('请输入要更新的包名称(多个包用半角逗号隔开)：').strip().rstrip(',')
pkg_list = pkg_str.split(',')

for pkg in pkg_list:
    print(f'正在安装{pkg}......')
    os.system(f'pip install --upgrade {pkg} -i https://pypi.tuna.tsinghua.edu.cn/simple')
    print('\n')

print('本次更新完成！')