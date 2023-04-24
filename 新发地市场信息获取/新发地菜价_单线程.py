# 100页 单线程  27.33s

import requests
import math
import pandas as pd
from tqdm import tqdm
import time


def download_one_page(page=1):
    base_url = 'http://www.xinfadi.com.cn/getPriceData.html'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-TW,zh;q=0.9,zh-CN;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '85',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'SHOP_MANAGE=fba385c2-2bc7-4701-bbd9-e6ea2a0b6849',
        'DNT': '1',
        'Host': 'www.xinfadi.com.cn',
        'Origin': 'http://www.xinfadi.com.cn',
        'Pragma': 'no-cache',
        'Referer': 'http://www.xinfadi.com.cn/priceDetail.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    datas = {
        'limit': '20',
        'current': str(page),
        'pubDateStartTime': '',
        'pubDateEndTime': '',
        'prodPcatid': '',
        'prodCatid': '',
        'prodName': '',
    }
    response = requests.post(url=base_url, headers=headers, data=datas)

    return response.json()


def datas_processing(html):
    for data in html['list']:
        data_info = {
            '一级分类': data['prodCat'],
            '二级分类': data['prodPcat'],
            '品名': data['prodName'],
            '最低价': data['lowPrice'],
            '平均价': data['avgPrice'],
            '最高价': data['highPrice'],
            '规格': data['specInfo'],
            '产地': data['place'],
            '单位': data['unitInfo'],
            '发布日期': data['pubDate'][:10],
        }
        yield data_info


def main():
    html = download_one_page(1)
    pages = math.ceil(int(html['count'])/20)
    results = []
    for page in tqdm(range(1, 101)):
        html = download_one_page(page)  # pages超过10000页，仅测试100页
        results.extend(datas_processing(html))

    files = pd.DataFrame(results)
    files.to_csv('新发地菜价_单线程.csv', index=False, encoding='utf-8-sig')

    print('下载完成！')


if __name__ == '__main__':
    t1 = time.time()
    main()
    t2 = time.time()
    print(t2-t1)
