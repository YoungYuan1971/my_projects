import requests

url = "https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/global.m3u"

res = requests.get(url)

with open("/mnt/sda2/iptv/iptv.m3u", mode='w', encoding='utf-8') as f:
    f.write(res.text)
