import requests
from SecretData import BAIDU_Account

# client_id 为官网获取的AK， client_secret 为官网获取的SK
AK = BAIDU_Account['API_KEY']
SK = BAIDU_Account['SECRET_KEY']

host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={AK}&client_secret={SK}'
response = requests.get(host)
if response.status_code == 200:
    result = response.json()
    print(result['access_token'])
