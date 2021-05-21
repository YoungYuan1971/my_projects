# -*- coding: UTF-8 -*- 
# @Time: 2020/11/20 10:04
# @Author: YoungYuan

import pyttsx3  # 文字转语音
import pdfplumber  # pdf文件解析

'''
# 调整语速，范围0-500
rate = engine.getProperty('rate')
engine.setProperty('rate', 200)
# 调整声量，范围0-1
volume = engine.getProperty('volume')
engine.setProperty('volume', 0.8)
# 保存音频到本地，格式为mp3
engine.save_to_file(text,f"{filename}.mp3")
engine.runAndWait()
'''


def text2speech(filename):
    engine = pyttsx3.init()
    pdf = pdfplumber.open(filename)
    pages = len(pdf.pages)
    for page in range(0, pages):
        print(f"总页数:{pages}  第{page + 1}页")
        print("-" * 80)
        content = pdf.pages[page]
        text = content.extract_text()
        print(text)
        print("=" * 80)
        text = text.replace('\n', "")
        engine.say(text)
        engine.runAndWait()


if __name__ == '__main__':
    file = "./Text2Speech.pdf"
    text2speech(file)
