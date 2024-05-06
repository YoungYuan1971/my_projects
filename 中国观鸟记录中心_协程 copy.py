import json
import csv
import asyncio
import aiohttp
import aiofiles
import execjs
from tqdm import tqdm


with open('中国观鸟记录中心_加解密.js', 'r', encoding='utf-8') as f:
    ctx = execjs.compile(f.read())

url = 'https://api.birdreport.cn/front/activity/search'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-TW,zh;q=0.9,zh-CN;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'DNT': '1',
    'Origin': 'http://birdreport.cn',
    'Pragma': 'no-cache',
    'Referer': 'http://birdreport.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'requestId': '',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sign': '',
    'timestamp': '',
}


def get_encryptedData(page):
    params = f"page={page}&limit=20"
    return ctx.call('encryptData', params)


def get_decryptedData(encryptedData):
    return ctx.call('decryptData', encryptedData)


async def send_request(page, session):
    encrypted_data = get_encryptedData(page)
    headers.update({
        'requestId': encrypted_data['requestId'],
        'sign': encrypted_data['sign'],
        'timestamp': str(encrypted_data['timestamp'])
    })
    data = encrypted_data['payload']
    async with session.post(url=url, headers=headers, data=data) as response:
        return await response.json()


async def save_data(page, session):
    async with aiofiles.open('中国观鸟记录中心.csv', 'a', encoding='utf-8-sig', newline='') as fin:
        writer = csv.writer(fin)
        result = await send_request(page, session)
        decrypted_data = json.loads(get_decryptedData(result['data']))
        for row in decrypted_data:
            data_field = [
                row.get('name'),
                row.get('timebegin'),
                row.get('timeend'),
                row.get('province_name'),
                row.get('city_name'),
                row.get('district_name'),
                row.get('point_name'),
                row.get('location'),
                row.get('username'),
                row.get('statistics')
            ]
            await writer.writerow(data_field)


async def main():
    while True:
        max_pages = input("请输入要爬取的页数：").strip()
        if not max_pages.isdigit():
            print("请输入数字!")
        else:
            break

    print("正在采集数据，请稍后...")
    with open('中国观鸟记录中心.csv', mode='w', encoding='utf-8-sig', newline='') as f:
        fieldnames = [
            'name',
            'timebegin',
            'timeend',
            'province_name',
            'city_name',
            'district_name',
            'point_name',
            'location',
            'username',
            'statistics'
        ]
        write_header = csv.DictWriter(f, fieldnames=fieldnames)
        write_header.writeheader()

    async with aiohttp.ClientSession() as session:
        tasks = []
        tasks = [asyncio.create_task(save_data(page, session))
                 for page in range(1, int(max_pages)+1)]
        [await task for task in tqdm(asyncio.as_completed(tasks), total=len(tasks))]

        await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())
