# 异步协程

import asyncio
import aiohttp
import aiofiles
from lxml import etree
import csv
from tqdm import tqdm
import time


async def download_one_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
    }
    async with aiofiles.open('新发地菜价_协程.csv', mode='a', encoding='utf-8', newline='') as fin:
        write_data = csv.writer(fin)
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                html = etree.HTML(await response.text())
                trs = html.xpath("//table[@class='hq_table']//tr")
                for tr in trs[1:]:
                    datas = tr.xpath("./td/text()")
                    await write_data.writerow(datas)


async def main():
    base_url = 'http://www.xinfadi.com.cn/marketanalysis/0/list/{}.shtml'
    print('正在下载......')
    tasks = []
    for page in range(1, 101):
        url = base_url.format(page)
        tasks.append(asyncio.create_task(download_one_page(url)))

    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        await task

    await asyncio.wait(tasks)
    print('下载完成！')


if __name__ == '__main__':
    t1 = time.time()
    with open('新发地菜价_协程.csv', mode='w', encoding='utf-8', newline='') as f:
        fieldnames = ['品名', '最低价', '平均价', '最高价', '规格', '单位', '发布日期']
        write_header = csv.DictWriter(f, fieldnames=fieldnames)
        write_header.writeheader()
    asyncio.run(main())
    t2 = time.time()
    print(t2-t1)
