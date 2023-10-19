import os
import requests
import re
from urllib.request import urlretrieve

path = './SignDesign'
base_url = 'http://www.kachayv.cn/'
 

def get_html(name, type):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }
    datas = {
        'word': name,
        'fonts': type,
        'sizes': '60',
        'fontcolor': '#ffffff',
        'colors': '#FD5668',
    }
    response = requests.post(base_url, headers=headers, data=datas)
    response.encoding = response.apparent_encoding

    return response.text


def get_img(html, filename):
    result = re.findall(r'<img id="showImg" src="(.*?)"/></div>', html)
    img_link = base_url+result[0]
    print(img_link)

    if not os.path.exists(path):
        os.mkdir(path)

    urlretrieve(url=img_link, filename=f'{path}/{filename}.png')
    print(f'完成！图片保存在{path}中。')


def main():
    name_input = input('请输入要设计的姓名：').strip()
    print('[1]花式签\n[2]商务签\n[3]个性签\n[4]手写连笔字\n[5]正楷体\n[6]温柔女生\n'
          '[7]潇洒签\n[8]超级艺术签\n[9]行书签\n[10]楷书签\n[11]情书签\n[12]行草签\n[13]卡通可爱签\n'
          '---------------\n[00]退出\n')
    type_input = input('请选择签名字体(仅输入数字):').strip()

    if type_input == '00':
        exit(0)
    elif not re.match(r"^[1-9]$|^[1][0-3]$", type_input):
        print('请输入正确的数字！')
    else:
        type_face = {
            '1': ['12.ttf', '花式签'],
            '2': ['16.ttf', '商务签'],
            '3': ['15.ttf', '个性签'],
            '4': ['9.ttf', '手写连笔字'],
            '5': ['17.ttf', '正楷体'],
            '6': ['13.ttf', '温柔女生'],
            '7': ['8.ttf', '潇洒签'],
            '8': ['7.ttf', '超级艺术签'],
            '9': ['6.ttf', '行书签'],
            '10': ['19.ttf', '楷书签'],
            '11': ['20.ttf', '情书签'],
            '12': ['11.ttf', '行草签'],
            '13': ['25.ttf', '卡通可爱签'],
        }
        html = get_html(name_input, type_face[type_input][0])
        get_img(html, name_input+'_'+type_face[type_input][1])


if __name__ == '__main__':
    main()
