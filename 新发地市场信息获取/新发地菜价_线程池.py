# 线程池


import requests
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor


def download_one_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    trs = html.xpath("//table[@class='hq_table']//tr")
    for tr in trs[1:]:
        datas = tr.xpath("./td/text()")
        write_data.writerow(datas)


if __name__ == '__main__':
    with open('新发地菜价_线程池.csv', mode='w', encoding='utf-8', newline='') as f:
        fieldnames = ['品名', '最低价', '平均价', '最高价', '规格', '单位', '发布日期']
        write_header = csv.DictWriter(f, fieldnames=fieldnames)
        write_header.writeheader()
        write_data = csv.writer(f)
        base_url = 'http://www.xinfadi.com.cn/marketanalysis/0/list/{}.shtml'
        print('正在下载......')
        with ThreadPoolExecutor(30) as pool:
            for page in range(1, 101):
                url = base_url.format(page)
                pool.submit(download_one_page, url)
        print('下载完成！')
