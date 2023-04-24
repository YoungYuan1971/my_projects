# -*- coding: UTF-8 -*- 
# @Time: 2020/11/9 12:29
# @Author: YoungYuan

import json


def get_code(stock_name):
    with open('./stock_code.json', mode='r', encoding='utf-8') as f:
        datas = json.load(f)
    if stock_name not in datas:
        return False
    else:
        return datas[stock_name]


if __name__ == '__main__':
    while True:
        print('Enter 000000 to exit!')
        name = input("Please Enter the StockName or StockCode:").strip()
        if name == '000000':
            exit(0)
        print(name, get_code(name), sep=': ')
