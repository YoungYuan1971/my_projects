# -*- coding: UTF-8 -*-
# @Time: 2021/04/19
# @Author: YoungYuan
# base_url：http://quote.eastmoney.com/center/gridlist.html#hs_a_board


import math
import pandas as pd
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures

MAX_WORKS = 30


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


def data_get(page):
    res_dic = web_get(page)
    datas = res_dic['data']['diff']
    df = pd.DataFrame(datas)

    return df


def main():
    # request the one page, get the total number of pages
    html = web_get(1)
    total = html['data']['total']
    pages = math.ceil(int(total) / 20)

    tasks = []
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKS) as pool:
        for page in range(1, pages + 1):
            tasks.append(pool.submit(data_get, page))

        for task in tqdm(futures.as_completed(tasks), total=len(tasks)):
            df = pd.DataFrame(task.result())
            results.append(df)

    # Data processing
    df_result = pd.concat(results)
    df_result = df_result[['f12', 'f14', 'f2', 'f3', 'f4',
                           'f5', 'f6', 'f7', 'f15', 'f16', 'f17', 'f9', 'f23']]
    rename = {
        'f12': '代码',
        'f14': '股票名称',
        'f2': '最新价',
        'f3': '涨跌幅',
        'f4': '涨跌额',
        'f5': '成交量/手',
        'f6': '成交额',
        'f7': '振幅',
        'f15': '最高',
        'f16': '最低',
        'f17': '今开',
        'f9': '动态PE',
        'f23': '静态PE',
    }
    df_result.rename(columns=rename, inplace=True)
    df_result.to_excel('Stock.xlsx', sheet_name='stock', index=False)

    print('Download complete!')


if __name__ == '__main__':
    main()
