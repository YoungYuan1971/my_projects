# -*- coding: UTF-8 -*-
# @Time: 2021/04/19
# @Author: YoungYuan
# base_url：http://quote.eastmoney.com/center/gridlist.html#hs_a_board


import math
import csv
import requests
from tqdm import tqdm
import asyncio
import aiohttp
import aiofiles


headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/86.0.4240.193 Safari/537.36 Edg/86.0.622.68',
    'DNT': '1',
    'Accept': '*/*',
    'Referer': 'http://quote.eastmoney.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}


async def web_get(page):
    params = {
        # 'cb': 'jQuery11240031572759315614984_1605253859898^',
        'pn': str(page) + '^',
        'pz': '20^',
        'np': '1^',
        'po': '1^',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281^',
        'fltt': '2^',
        'invt': '2^',
        'fid': 'f3^',
        'fs': 'm:0 t:6,m:0 t:13,m:0 t:80,m:1 t:2,m:1 t:23^',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,'
                  'f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152^',
        # '_': '1605253859908',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get('http://67.push2.eastmoney.com/api/qt/clist/get', headers=headers,
                               params=params) as response:

            content = await response.json()
            return content


async def data_get(page):
    async with aiofiles.open('Stock.csv', 'a', encoding='utf-8-sig', newline='') as fin:
        data_writer = csv.writer(fin)

        res_dic = await web_get(page)
        datas = res_dic['data']['diff']
        for data in datas:
            data_info = [
                data['f12'], data['f14'], data['f2'], data['f3'], data['f4'], data['f5'],
                data['f6'], data['f7'], data['f15'], data['f16'], data['f17'], data['f9'], data['f23'],
            ]

            await data_writer.writerow(data_info)


async def main(pages):
    tasks = [asyncio.create_task(data_get(page)) for page in range(1, pages + 1)]

    [await task for task in tqdm(asyncio.as_completed(tasks), total=len(tasks))]
        
    await asyncio.wait(tasks)

    print('Download complete!')


if __name__ == '__main__':
    base_url = 'http://39.push2.eastmoney.com/api/qt/clist/get?' \
        'pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281' \
        '&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23' \
        '&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,' \
        'f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'

    # request the one page, get the total number of pages
    html = requests.get(base_url, headers=headers)
    total = html.json()['data']['total']
    pages = math.ceil(int(total) / 20)

    with open('Stock.csv', 'w', encoding='utf-8-sig', newline='') as f:
        field_name = [
            '代码', '股票名称', '最新价', '涨跌幅', '涨跌额', '成交量/手',
            '成交额', '振幅', '最高', '最低', '今开', '动态PE', '静态PE',
        ]
        field_writer = csv.DictWriter(f, fieldnames=field_name)
        field_writer.writeheader()

    asyncio.run(main(pages))
