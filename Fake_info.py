# -*- coding: UTF-8 -*- 
# @time: 2021/3/16 17:21
# @file: fake_info.py
# @Author: YoungYuan


import pandas as pd
from faker import Faker
from tqdm import tqdm


def generate(n):
    datas = []
    for _ in tqdm(range(n)):
        data_info = {
            '姓名': fake.name(),
            '电话': fake.phone_number(),
            '出生日期': fake.date(),
            '公司': fake.company(),
            '职位': fake.job(),
            '地址': fake.address(),
            '电子邮件': fake.email(),
        }
        datas.append(data_info)

    return datas


if __name__ == '__main__':
    total = 100000
    fake = Faker(locale='zh_CN')
    df = pd.DataFrame(generate(total))
    df.to_excel('fake_info.xlsx', index=False)
