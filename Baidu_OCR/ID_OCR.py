import os
import pandas as pd
from aip import AipOcr
from SecretData import BAIDU_OCR

APP_ID = BAIDU_OCR['APP_ID']
API_KEY = BAIDU_OCR['API_KEY']
SECRET_KEY = BAIDU_OCR['SECRET_KEY']
# 传递鉴权信息并实例化对象
CLIENT = AipOcr(appId=APP_ID, apiKey=API_KEY, secretKey=SECRET_KEY)


def find_all_img(base_path):
    for root, _, fs in os.walk(base_path):
        for f in fs:
            if f.endswith(('.jpeg', '.jpg', '.png')):
                yield root + '/' + f


def img_ocr(img):
    try:
        with open(img, 'rb') as fp:
            # res = client.basicAccurate(fp.read())  # 高精度，500次/天/免费
            res = CLIENT.basicGeneral(fp.read())  # 标准版，50000次/天/免费
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
                    ids = row[6:]
                else:
                    addr += row

            data_info = {
                '姓名': name,
                '性别': gender,
                '民族': nation,
                '出生日期': birth,
                '住址': addr,
                '身份证号码': ids,
                '文件名': img
            }

            return data_info

    except:
        fail_path = 'ID_Fail'
        if not os.path.exists(fail_path):
            os.mkdir(fail_path)
        os.system(f'mv {img} {fail_path}/')  # 将识别失败的文件转移到统一目录下
        print(f'{img}识别失败，已移到{fail_path}目录下！')

        return False


def main():
    base_path = '身份证'
    imgs = find_all_img(base_path)
    datas = []
    for img in imgs:
        print(f'正在识别{img}......')
        result = img_ocr(img)
        if not result:
            continue
        datas.append(result)

    df = pd.DataFrame(datas)
    df.to_excel('./ID.xlsx', index=False)
    print('识别完成，数据写入[ID.xlsx]文件中！')


if __name__ == '__main__':
    main()
