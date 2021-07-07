from aip import AipOcr
from SecretData import BAIDU_Account


APP_ID = BAIDU_Account['APP_ID']
API_KEY = BAIDU_Account['API_KEY']
SECRET_KEY = BAIDU_Account['SECRET_KEY']


def ocr_run():
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    with open('/Users/youngyuan/PythonProjects/身份证识别_OCR/身份证/ID_001.jpeg', 'rb') as fp:
        res = client.basicAccurate(fp.read())
        for data in res['words_result']:
            # print(data)
            row = data['words']
            if '姓名' in row:
                name = row[2:]
            elif '性别' in row:
                gender = row[2:3]
                nation = row[5:]
            elif '出生' in row:
                birth = row[2:]
            elif '住址' in row:
                addr = row[2:]
            elif '公民身份号码' in row:
                id = row[6:]
            else:
                addr += row

        return name, gender, nation, birth, addr, id


if __name__ == '__main__':
    result = list(ocr_run())
    print(result)
