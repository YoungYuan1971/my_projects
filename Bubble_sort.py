import random

li = [random.randint(1, 100) for n in range(20)]  # 随机生成N个[1-100]的整数列表

print(f'Before:{li}')
for i in range(len(li) - 1):  # 控制比较次数
    for j in range(i + 1, len(li)):  # 控制列表下标
        if li[i] > li[j]:
            li[i], li[j] = li[j], li[i]  # 数值交换
print(f'After:{li}')
