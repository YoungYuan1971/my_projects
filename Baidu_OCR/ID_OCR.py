# -*- coding: UTF-8 -*-
# @time: 2022/7/6 11:05
# @file: ID_OCR.py
# @Author: YoungYuan


import os
import time
import shutil
from aip import AipOcr
from SecretData import BAIDU_OCR
import BaiduOCR_IO


class OCR(AipOcr):  # 继承类
    def __init__(self, imgs):  # 魔术方法，重构函数
        BAIDU = BAIDU_OCR()
        super().__init__(appId=BAIDU.APP_ID, apiKey=BAIDU.API_KEY,
                         secretKey=BAIDU.SECRET_KEY)  # 初始化基类
        self.imags = imgs
        self.pic = ''

    def baidu_ocr(self):
        results = []
        for self.pic in self.imags:
            print(f'正在识别{self.pic}......')
            try:
                with open(self.pic, 'rb') as fp:
                    res = self.idcard(fp.read(), 'front')[
                        'words_result']  # 500次/天免费
                    # print(res)
                    results.append(self.paser_data(res))
                    time.sleep(1)

            except Exception as e:
                print(e)
                fail_path = 'ID_Fail'
                if not os.path.exists(fail_path):
                    os.mkdir(fail_path)
                shutil.move(self.pic, fail_path)
                print(f'{self.pic}识别失败，已移到{fail_path}目录下！')

        BaiduOCR_IO.save_file('ID.xlsx', results)
        print('识别完成，数据写入[ID.xlsx]文件中！')

    def paser_data(self, data):
        name = data["姓名"]["words"]
        gender = data["性别"]["words"]
        nation = data["民族"]["words"]
        birth = f'{data["出生"]["words"][0:4]}-{data["出生"]["words"][4:6]}-{data["出生"]["words"][6:]}'
        address = data["住址"]["words"]
        id_number = data["公民身份号码"]["words"]

        data_info = {
            '姓名': name,
            '性别': gender,
            '民族': nation,
            '出生日期': birth,
            '住址': address,
            '身份证号码': id_number,
            '文件名': self.pic
        }

        return data_info


def main():
    print('------------------------------')
    print('支持的图片格式：jpg;jpeg;png;bmp')
    print('------------------------------')
    base_path = 'ID_Card'
    imgs = BaiduOCR_IO.find_all_img(base_path)
    app = OCR(imgs)
    app.baidu_ocr()


if __name__ == '__main__':
    main()
