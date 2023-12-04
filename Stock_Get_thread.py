# -*- encoding: utf-8 -*-
'''
@File    :   Stock_Get_thread.py
@Time    :   2023/12/04 09:45:37
@Author  :   YoungYuan 
@Contact :   young_yuan@hotmail.com
@License :   (C)Copyright 2022-2031, YoungYuan
'''


import math
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import pandas as pd
from tqdm import tqdm


class StockCrawl:

    def __init__(self):
        self.url = "https://63.push2.eastmoney.com/api/qt/clist/get"
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,zh;q=0.9,zh-CN;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'qgqp_b_id=62c04a4e98d54385d4f24409507674b5; intellpositionL=1237.58px; cowminicookie=true; '
            'cowCookie=true; st_si=73868227870871; st_asi=delete; intellpositionT=455px; st_pvi=76856893471525; '
            'st_sp=2021-11-10%2008%3A32%3A30; st_inirUrl=http%3A%2F%2Fdata.eastmoney.com%2Fcenter%2F; st_sn=12; '
            'st_psi=20211124105240665-113200301321-5546042617',
            'DNT': '1',
            'Host': '63.push2.eastmoney.com',
            'Referer': 'https://quote.eastmoney.com/',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/95.0.4638.69 Safari/537.36',
        }
        self.params = {
            'pn': "",
            'pz': '20',
            'po': '1',
            'np': '1',
            'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
            'fltt': '2',
            'invt': '2',
            'fid': 'f3',
            'fs': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048',
            'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152',
        }

    def get_data(self, pn):
        self.params.update(pn=str(pn))
        response = requests.get(
            self.url, headers=self.headers, params=self.params)
        return response.json()

    def parse_data(self, page_num):
        datas = self.get_data(page_num)['data']['diff']
        for data in datas:
            data_info = {
                '代码': data['f12'],
                '名称': data['f14'],
                '最新价': data['f2'],
                '涨跌幅': data['f3'],
                '涨跌额': data['f4'],
                '成交量(手)': data['f5'],
                '成交额': data['f6'],
                '振幅': data['f7'],
                '最高价': data['f15'],
                '最低价': data['f16'],
                '今开': data['f17'],
                '昨收': data['f18'],
                '量比': data['f10'],
                '换手率': data['f8'],
                '市盈率(动态)': data['f9'],
                '市净率': data['f23'],
            }
            yield data_info

    def crawl(self):
        pages = math.ceil(self.get_data(1)['data']['total'] / 20)
        results = []
        with ThreadPoolExecutor(50) as pool:
            tasks = [pool.submit(self.parse_data, page)
                     for page in range(1, pages + 1)]
            [results.extend(task.result())
             for task in tqdm(as_completed(tasks), total=len(tasks))]

        df = pd.DataFrame(results)
        df.to_csv('stock_info.csv', index=False)

        print("数据信息已下载完成！")


if __name__ == '__main__':
    stock_crawl = StockCrawl()
    stock_crawl.crawl()
