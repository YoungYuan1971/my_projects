"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
# 示例下载 https://www.pytk.net/blog/1702564569.html

import re
from urllib import parse
import webbrowser
import tkinter
from tkinter import messagebox
from ui import Win


class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: Win

    def __init__(self):
        pass

    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        # TODO 组件初始化 赋值操作
        self.channel = tkinter.IntVar()
        self.channel.set(1)
        self.ui.tk_radio_button_channel_one.configure(
            value=1, variable=self.channel)
        self.ui.tk_radio_button_channel_two.configure(
            value=2, variable=self.channel)
        self.ui.tk_radio_button_channel_three.configure(
            value=3, variable=self.channel)

    def play_video(self, evt):
        port = {
            1: "https://im1907.top/?jx=",
            2: "https://bd.jx.cn/?url=",
            3: "https://jx.m3u8.tv/jiexi/?url="
        }
        key = self.channel.get()
        API = port[key]
        if re.match(r'https?:/{2}\w.+$', play_url := self.ui.tk_input_play_url.get()):
            # 对含有特殊符号的 URL 进行编码，使其转换为合法的 url 字符串
            play_url = parse.quote_plus(play_url)
            webbrowser.open(API + play_url)
            self.ui.destroy()
        else:
            messagebox.showwarning(title="错误", message="视频地址无效，请重新输入！")

    def destroy(self, evt):
        self.ui.destroy()
