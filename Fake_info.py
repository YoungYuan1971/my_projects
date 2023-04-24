# -*- coding: UTF-8 -*-
# @time: 2021/3/16 17:21
# @file: fake_info.py
# @Author: YoungYuan


import pandas as pd
from faker import Faker
from tqdm import tqdm


def generate(n):
    for _ in tqdm(range(n)):
        data_info = {
            'Name': fake.name(),
            'Telephone': fake.phone_number(),
            'Birth': fake.date(),
            'Company': fake.company(),
            'Position': fake.job(),
            'Address': fake.address(),
            'Email': fake.email(),
        }
        yield data_info


if __name__ == '__main__':
    total = 100000
    fake = Faker(locale='en_US')  # 设置中文：locale='zh_CN'
    df = pd.DataFrame(generate(total))
    df.to_csv('fake_info.csv', index=False)
