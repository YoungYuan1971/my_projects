# -*- coding: UTF-8 -*- 
# @time: 2021/7/15 13:37
# @file: BaiduOCR_IO.py
# @Author: YoungYuan

import os
import pandas as pd

ImgType = ('jpg', 'jpeg', 'png', 'bmp')


def find_all_img(path):
    if not os.path.exists(path):
        print(f'请在本目录下新建名为{path.split("/")[0]}的目录，将需要扫描的图片放入该目录！')
        exit(0)
    for root, _, fs in os.walk(path):
        for f in fs:
            if f.endswith(ImgType):
                yield path.rstrip('/') + '/' + f


def save_file(file_name, df):
    df = pd.DataFrame(df)
    fileName = file_name.split(".")[0]
    df.to_excel(f'{fileName}.xlsx', sheet_name=f'{fileName}', index=False)


if __name__ == '__main__':
    base_path = 'IDCard_OCR/ID_Source'
    imgs = find_all_img(base_path)
    print(list(imgs))
    data_frame = [{'name': '1', 'age': 18}, {'name': '2', 'age': 20}, {'name': '3', 'age': 30}]
    save_file('example', df=data_frame)
