import time
import requests


# Base_url: https://github.com/fanmingming/live/

url = "https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/global.m3u"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'raw.githubusercontent.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15',
}

try:
    res = requests.get(url, headers=headers)

    with open("iptv.m3u", mode='w', encoding='utf-8') as f:
        f.write(res.text)
        
    update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"于{update_time}...下载成功！")

except Exception as e:
    print(f"下载失败！{e}")
    time.sleep(1)
    pass


