# -*- encoding: utf-8 -*-
'''
@File    :   极简壁纸.py
@Time    :   2024/04/15 10:39:47
@Author  :   YoungYuan 
@Contact :   young_yuan@hotmail.com
@License :   (C)Copyright 2022-2031, YoungYuan
'''

import os
import asyncio
import aiohttp
import aiofiles
import requests
import execjs
from tqdm import tqdm


if not os.path.exists(path := '极简壁纸'):
    os.mkdir(path)

with open('极简壁纸_逆向.js', 'r', encoding='utf-8') as f:
    ctx = execjs.compile(f.read())

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-TW,zh;q=0.9,zh-CN;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'dnt': '1',
    'origin': 'https://bz.zzzmh.cn',
    'pragma': 'no-cache',
    'referer': 'https://bz.zzzmh.cn/',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

json_data = {
    'size': 24,
    'current': '',
    'sort': 0,
    'category': 0,
    'resolution': 0,
    'color': 0,
    'categoryId': 0,
    'ratio': 0,
}


def get_ciphertext(json_data):
    url = 'https://api.zzzmh.cn/bz/v3/getData'
    return requests.post(url, headers=headers, json=json_data).json()


def decrypt_data(ciphertext):
    return ctx.call('decryptData', ciphertext)


async def download_img(url, session):
    async with session.get(url, headers=headers) as response:
        return await response.read()  # read()返回二进制数据; json()返回json数据； text()返回字符串数据


async def save_img(img_url, session):
    img_data = await download_img(img_url, session)
    async with aiofiles.open(f'{path}/{img_url.split("/")[-1]}.png', 'wb') as f:
        await f.write(img_data)


async def main():
    pages = int(input('请输入要爬取的页数：').strip())
    for page in tqdm(range(1, pages+1)):
        json_data['current'] = page
        ciphertext = get_ciphertext(json_data)['result']
        plaintext = decrypt_data(ciphertext)
        async with aiohttp.ClientSession() as session:
            tasks = []
            for result in plaintext['list']:
                img_url = f"https://api.zzzmh.cn/bz/v3/getUrl/{result['i']}{result['t']}1"
                tasks.append(asyncio.create_task(save_img(img_url, session)))

            await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())
