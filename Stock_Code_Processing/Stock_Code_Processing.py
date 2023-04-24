# -*- coding: UTF-8 -*-
# @Time: 2020/11/12 14:20
# @Author: YoungYuan
# 东方财富网原始网页：http://data.eastmoney.com/zjlx/detail.html

import math
import requests
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


def web_get(page):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63',
        'DNT': '1',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    param = (
        ('pn', str(page) + '^'),
        ('pz', '50^'),
        ('po', '1^'),
        ('np', '1^'),
        ('ut', 'b2884a393a59ad64002292a3e90d46a5^'),
        ('fltt', '2^'),
        ('invt', '2^'),
        ('fid0', 'f4001^'),
        ('fid', 'f62^'),
        ('fs', 'm:0 t:6 f:^!2,m:0 t:13 f:^!2,m:0 t:80 f:^!2,m:1 t:2 f:^!2,m:1 t:23 f:^!2,m:0 t:7 f:^!2,m:1 t:3 f:^!2^'),
        ('stat', '1^'),
        ('fields', 'f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124^'),
        ('rt', '53505436^'),
        # ('cb', 'jQuery18307362461875553439_1605163088229^'),
        ('_', '1605163089114'),
    )
    session = requests.Session()
    response = session.get('http://push2.eastmoney.com/api/qt/clist/get',
                           headers=headers, params=param, verify=False)
    return response.text


def data_processing(page):
    html = web_get(page)
    datas = json.loads(html)['data']['diff']

    result = {}
    [result.update({data['f14']: data['f12'], data['f12']:data['f14']}) for data in datas]

    return result


def main():
    html = json.loads(web_get(1))  # 先请求第一页，获取数据总数，以便统计页数
    total = html['data']['total']
    pages = math.ceil(int(total) / 50)  # 向上取整

    results = {}
    with open('./stock_code.json', 'w', encoding='utf-8') as fin:
        with ThreadPoolExecutor(30) as pool:
            tasks = [pool.submit(data_processing, page)
                     for page in range(1, pages + 1)]

            [results.update(task.result()) for task in tqdm(
                as_completed(tasks), total=len(tasks))]

        json.dump(results, fin, ensure_ascii=False)


if __name__ == '__main__':
    main()
