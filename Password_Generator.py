import string
import random
import re


def gen_pwd(number):
    str = string.ascii_letters+string.digits+string.punctuation
    password = ''.join(random.choice(str) for _ in range(0, number))

    return password


if __name__ == '__main__':
    n = input('请输入要生成的密码位数：').strip()
    if re.fullmatch(r'\d+', n):
        pwd = gen_pwd(int(n))
        print(f'生成的密码是：{pwd}')
    else:
        print('错误的输入，请输入数字！')
