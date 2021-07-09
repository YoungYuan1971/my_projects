import requests
from SecretData import BAIDU_Account

# client_id 为官网获取的AK， client_secret 为官网获取的SK
AK = BAIDU_Account['API_KEY']
SK = BAIDU_Account['SECRET_KEY']


def token_get():
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={AK}&client_secret={SK}'
    response = requests.get(host)
    if response.status_code == 200:
        ressult = response.json()
        access_token = ressult['access_token']

        return access_token


if __name__ == '__main__':
    print(token_get())
