# 100页 异步协程  3.50s

import asyncio
import aiohttp
import aiofiles
import csv
from tqdm import tqdm
import time


async def download_one_page(page=1):
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

    async with aiohttp.ClientSession() as session:
        async with session.post(url=base_url, headers=headers, data=datas) as response:

            return await response.json()


async def save_datas(page):
    async with aiofiles.open('新发地菜价_协程.csv', 'a', encoding='utf-8-sig', newline='') as fin:
        writer = csv.writer(fin)
        datas = await download_one_page(page)
        for data in datas['list']:
            data_field = [
                data['prodCat'], data['prodPcat'], data['prodName'], data['lowPrice'],
                data['avgPrice'], data['highPrice'], data['specInfo'], data['place'],
                data['unitInfo'], data['pubDate'][:10],
            ]

            await writer.writerow(data_field)


async def main():
    tasks = [asyncio.create_task(save_datas(page)) for page in range(1, 101)]
    [await task for task in tqdm(asyncio.as_completed(tasks), total=len(tasks))]

    await asyncio.wait(tasks)
    
    print('下载完成！')


if __name__ == '__main__':
    t1 = time.time()
    with open('新发地菜价_协程.csv', mode='w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['一级分类', '二级分类', '品名', '最低价',
                      '平均价', '最高价', '规格', '产地', '单位', '发布日期']
        write_header = csv.DictWriter(f, fieldnames=fieldnames)
        write_header.writeheader()
    asyncio.run(main())
    t2 = time.time()
    print(t2-t1)
