import string
import random
import re


def gen_pwd(n):
    str = string.ascii_letters+string.digits+string.punctuation
    password = ''.join(random.choice(str) for _ in range(0, n))

    return password


if __name__ == '__main__':
    number = input('请输入要生成的密码位数：').strip()
    if re.fullmatch(r'\d+', number):
        pwd = gen_pwd(int(number))
        print(pwd)
    else:
        print('错误的输入，请输入数字！')
