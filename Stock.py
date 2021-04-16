# -*- coding: UTF-8 -*-
# @Time: 2020/11/13 15:52
# @Author: YoungYuan
# 东方财富网原始网页：http://quote.eastmoney.com/center/gridlist.html#hs_a_board(沪深A股)

import json
import math
import os
import time
import pandas as pd
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures
import csv


def web_get(page):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.193 Safari/537.36 Edg/86.0.622.68',
        'DNT': '1',
        'Accept': '*/*',
        'Referer': 'http://quote.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    params = (
        # ('cb', 'jQuery11240031572759315614984_1605253859898^'),
        ('pn', str(page) + '^'),
        ('pz', '20^'),
        ('po', '1^'),
        ('np', '1^'),
        ('ut', 'bd1d9ddb04089700cf9c27f6f7426281^'),
        ('fltt', '2^'),
        ('invt', '2^'),
        ('fid', 'f3^'),
        ('fs', 'm:0 t:6,m:0 t:13,m:0 t:80,m:1 t:2,m:1 t:23^'),
        ('fields',
         'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152^'),
        ('_', '1605253859908'),
    )
    session = requests.Session()
    response = session.get('http://67.push2.eastmoney.com/api/qt/clist/get', headers=headers,
                           params=params, verify=False)
    return response.json()


def date_save(page):
    response = web_get(page)
    datas = response['data']['diff']

    for data in datas:
        results = [
            data['f12'],
            data['f14'],
            data['f2'],
            data['f3'],
            data['f4'],
            data['f5'],
            data['f6'],
            data['f7'],
            data['f15'],
            data['f16'],
            data['f17'],
            data['f9'],
            data['f23'],
        ]
        writer.writerow(results)


def main():
    html = web_get(1)  # 先请求第一页，获取数据总数，以便统计页数
    total = html['data']['total']
    pages = math.ceil(int(total) / 20)  # 向上取整
    tasks = []
    with ThreadPoolExecutor(30) as pool:
        for page in range(1, pages+1):
            # if page % 50 == 0:
            #     time.sleep(3)
            tasks.append(pool.submit(date_save, page))

        for _ in tqdm(futures.as_completed(tasks), total=len(tasks)):
            pass

    print(f'数据已保存在"{path}"目录下！')


if __name__ == '__main__':
    path = "./综合类"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(f'{path}/stock.csv', mode='w', newline='') as f:
        fieldnames = [
            '代码',
            '股票名称',
            '最新价',
            '涨跌幅',
            '涨跌额',
            '成交量/手',
            '成交额',
            '振幅',
            '最高价',
            '最低价',
            '今开',
            '动态PE',
            '静态PE'
        ]
        header_writer = csv.DictWriter(f, fieldnames=fieldnames)
        header_writer.writeheader()
        writer = csv.writer(f)
        main()
