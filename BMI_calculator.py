from pywebio.input import *
from pywebio.output import *


def bmi(height, weight):  # 计算BMI
    bmi_value = weight / (height / 100) ** 2
    top_status = [(14.9, '极瘦'), (18.4, '偏瘦'),
                  (22.9, '正常'), (27.5, '过重'),
                  (40.0, '肥胖'), (float('inf'), '非常肥胖')]

    for top, status in top_status:
        if bmi_value <= top:
            return bmi_value, status


def main():
    height = input("请输入你的身高(cm)：", type=FLOAT)
    weight = input("请输入你的体重(kg)：", type=FLOAT)

    bmi_value, status = bmi(height, weight)

    put_text('你的 BMI 值: %.1f，身体状态：%s' % (bmi_value, status))


if __name__ == '__main__':
    main()
