import requests
import pandas as pd

# 直接展示每页9999条数据，直接暴力获取
url = 'http://31.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=9999&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1689749812327'

headers = {
    'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

response = requests.get(url, headers=headers)
datas = response.json()

result = []
for data in datas['data']['diff']:
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
        '市净率': data['f23']
    }
    result.append(data_info)


df = pd.DataFrame(result)
df.to_csv('stock.csv', index=False)

print("数据信息已下载完成！")