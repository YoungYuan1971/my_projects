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
    'DNT': '1',
    'Host': '83.push2.eastmoney.com',
    'Referer': 'https://quote.eastmoney.com/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}


async def html_get(page):
    url = 'https://63.push2.eastmoney.com/api/qt/clist/get'
    params = {
        # 'cb': 'jQuery112402374539779714402_1637721974443',
        'pn': str(page),
        'pz': '20',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,'
                  'f136,f115,f152',
        # '_': '1637721974505',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, params=params) as response:
            return await response.json()


async def data_get(page):
    html = await html_get(page)
    datas = html['data']['diff']

    async with aiofiles.open("stock.csv", "a", newline="") as fp:
        writer = csv.writer(fp)

        for data in datas:
            data_info = [
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
                data['f18'],
                data['f10'],
                data['f8'],
                data['f9'],
                data['f23'],
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
    base_url = "https://83.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1" \
               "&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=3323094401493896|0|1|0|web" \
               "&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048" \
               "&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21," \
               "f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1672038419597"
    html_first_page = requests.get(url=base_url, headers=headers).json()

    pages = math.ceil(html_first_page['data']['total'] / 20)

    with open("stock.csv", "w") as fin:
        field_name = ['代码', '名称', '最新价', '涨跌幅', '涨跌额', '成交量(手)', '成交额', '振幅',
                      '最高价', '最低价', '今开', '昨收', '量比', '换手率', '市盈率(动态)', '市净率']
        header_writer = csv.DictWriter(fin, field_name)
        header_writer.writeheader()

    asyncio.run(main(pages))
