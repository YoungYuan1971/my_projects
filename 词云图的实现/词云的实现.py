# -*- coding: UTF-8 -*-
# @Time: 2020/11/9 12:29
# @Author: YoungYuan

import jieba
from wordcloud import WordCloud
import numpy as np
import PIL.Image as image


def get_txt(file):
    with open(file, 'r', encoding='u8') as f:
        strs = " ".join(f.readlines())
    word_lst = jieba.lcut(strs)
    return " ".join(word_lst)


def stop_words():
    with open('词云_stopwords.txt', 'r') as f:
        lst = f.readlines()
        stop_word_lst = [x.strip('\n') for x in lst]

    return stop_word_lst


def get_wordcloud(word):
    mask = np.array(image.open("Apple.png"))  # 设置词云图形状，背景色必须位白色，否则会生成矩形
    wc = WordCloud(
        mask=mask,
        font_path='./PingFang.ttc',
        background_color='black',
        max_words=1000,
        width=1080,
        height=720,
    )
    wc.stopwords = stop_words()
    wc.generate(word)
    wc.to_file('./词云图.png')  # 保存图片
    wc_image = wc.to_image()
    wc_image.show()  # 显示图片


def main(filename):
    txt_str = get_txt(filename)
    get_wordcloud(txt_str)


if __name__ == '__main__':
    main('词云文本.txt')
