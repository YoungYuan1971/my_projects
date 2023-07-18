# -*- coding: UTF-8 -*-
# @time: 2021/11/24 10:55
# @file: 东方财富网_股票行情.py
# @Author: YoungYuan
# https://quote.eastmoney.com/center/gridlist.html#hs_a_board 沪深京A股


import csv
import math
import asyncio
import aiohttp
import aiofiles
import requests
from tqdm import tqdm

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-TW,zh;q=0.9,zh-CN;q=0.8',
    'Cache-Control': 'no-cache',
    'DNT': '1',
    'Host': '20.push2.eastmoney.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}


async def html_get(page):
    url = 'http://20.push2.eastmoney.com/api/qt/clist/get'
    params = {
        'pn': '1',
        'pz': '20',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'wbp2u': '|0|0|0|web',
        'fid': 'f3',
        'fs': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, params=params) as response:
            return await response.json()


async def data_get(page):
    html = await html_get(page)
    datas = html['data']['diff']

    async with aiofiles.open("stock_info.csv", "a", newline="") as fp:
        writer = csv.writer(fp)

        for data in datas:
            data_info = [
                data.get('f12', ''),
                data.get('f14', ''),
                data.get('f2', ''),
                data.get('f3', ''),
                data.get('f4', ''),
                data.get('f5', ''),
                data.get('f6', ''),
                data.get('f7', ''),
                data.get('f15', ''),
                data.get('f16', ''),
                data.get('f17', ''),
                data.get('f18', ''),
                data.get('f10', ''),
                data.get('f8', ''),
                data.get('f9', ''),
                data.get('f23', ''),
            ]
            await writer.writerow(data_info)


async def main(pages):
    tasks = []

    for page in range(1, pages + 1):
        tasks.append(asyncio.create_task(data_get(page)))

    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        await task

    await asyncio.wait(tasks)


if __name__ == '__main__':
    base_url = "http://20.push2.eastmoney.com/api/qt/clist/get?" \
        "pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&" \
        "fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&" \
        "fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17," \
        "f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152"
    html_first_page = requests.get(url=base_url, headers=headers).json()

    pages = math.ceil(html_first_page['data']['total'] / 20)

    with open("stock_info.csv", "w") as fin:
        field_name = ['代码', '名称', '最新价', '涨跌幅', '涨跌额', '成交量(手)', '成交额', '振幅',
                      '最高价', '最低价', '今开', '昨收', '量比', '换手率', '市盈率(动态)', '市净率']
        header_writer = csv.DictWriter(fin, field_name)
        header_writer.writeheader()

    asyncio.run(main(pages))
