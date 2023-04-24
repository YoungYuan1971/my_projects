# 百度翻译js逆向解析

import re
import requests
import execjs

target_lang = {
    "1": ("zh", "en"),
    "2": ("en", "zh"),
    "3": ("zh", "jp"),
    "4": ("jp", "zh"),
    "5": ("zh", "fra"),
    "6": ("fra", "zh"),
}

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.9,zh-CN;q=0.8',
    'Connection': 'keep-alive',
    # 'Content-Length': '134',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'BIDUPSID=9FD3E7348F0150D2A227913A3C2F0E2E; PSTM=1638792239; BAIDUID=D8763997675317B3D9AD6BA5FA74C87C:FG=1; BAIDUID_BFESS=D8763997675317B3D9AD6BA5FA74C87C:FG=1; __yjs_duid=1_a3a7327a8543bbcc8d2d528e8781820a1638927092692; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDU_WISE_UID=wapp_1639636795074_87; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1639999048,1640047298,1640054284; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1640054284; __yjs_st=2_YTZlZmFmYjIyODVjZWRhMTg1YzU4OGNjNjMwNWJmYTc4MGRmMGI1YTM4OTY4NzNkODYzMzAxZTY3NTFmMzI0OTdmYmQ5MWUyNmU4N2U3YmVmNDNiYzc3Y2EyZGY1ZmY5M2UxZmE1MDg0OGZlYjEwOGZhMjUwNWFmNTMxY2FlOGUyZDJhNDg2NGNhOTllZWExODA0MDViMWVhMjVjNWI3NjRkMTRkNDJiOTFhMDA1ZjFkY2M2MWJjNjk2MzFmMTk1ODIyYTNiZjBhY2VmMGJlYjVmNmY4MzQ4YWI1YzI0ZWU2NTQxMjkxNmNiY2Y0ZGIzNTI0MmUyNWI1MGRlZWJjNV83XzllN2E2ZDIy; ab_sr=1.0.1_NmVjZTU2MzE3OTEwMTcxZjQzOGQwMmYyNmFkZjg4MmY2MzE5NGZiMzVkNDI2MThlOGYzNTY1YjI1MjI1MjA4OGFiZjA2NzMwY2ZhNjkxZjdmY2NjODdiOGVlNTQ4YzYwMDU4YWJmYmU0MmUzMGQzOWY0MDM1ZTJlMTYxZDdmYjk0ZGZmZjY1N2RkZTZkZjFhNDJlNjJlMjMxOTc3ZmI3Nw==',
    'DNT': '1',
    'Host': 'fanyi.baidu.com',
    'Origin': 'https://fanyi.baidu.com',
    'Referer': 'https://fanyi.baidu.com/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def get_html(query, s_lang, t_lang, token, sign):
    url = "https://fanyi.baidu.com/v2transapi"
    data = {
        'from': s_lang,
        'to': t_lang,
        'query': query,
        'transtype': 'realtime',
        'simple_means_flag': '3',
        'sign': sign,
        'token': token,  # 固定值，在网页源码中匹配
        'domain': 'common',
    }
    response = requests.post(url, headers=headers, data=data)
    response.encoding = response.apparent_encoding
    return response.json()


def get_token():
    res = requests.get("https://fanyi.baidu.com/#auto/zh/", headers=headers)
    token = re.findall(r"token: '(.*?)',", res.text, re.S)[0]
    return token


def get_sign(word):
    node = execjs.get()
    with open('./baidu_encrypt.js', 'r', encoding='utf-8') as f:
        baidu_js = f.read()
    ctx = node.compile(baidu_js)
    sign = ctx.call('getSign', word)
    return sign


def main():
    while True:
        print("1. 中文>>>英语\n2. 英语>>>中文\n3. 中文>>>日语\n4. 日语>>>中文\n5. 中文>>>法语\n6. 法语>>>中文\n0. 退出")
        choice_lang = input("请选择要翻译的语种(数字): ").strip()
        if not re.match(r"^[0-6]$", choice_lang):
            print("输入的数字错误!")
            break
        if choice_lang == "0":
            break
        from_lang = target_lang[choice_lang][0]
        to_lang = target_lang[choice_lang][1]
        word = input("请输入要翻译的内容: ").strip()
        token = get_token()
        sign = get_sign(word)
        results = get_html(word, from_lang, to_lang, token, sign)
        dict_result = results.get('dict_result')
        if dict_result:
            dict_result = "; ".join(dict_result['simple_means']['word_means'])
            print(dict_result)
        else:
            trans_result = results.get('trans_result')['data'][0]['dst']
            print(trans_result)

        print("-"*120)


if __name__ == '__main__':
    main()
