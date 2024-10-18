import re
import tkinter as tk
from tkinter import messagebox as msgbox
from urllib import parse
import webbrowser


class Application(tk.Tk):  # 继承tkinter类
    def __init__(self):  # 魔术方法，重构函数
        super().__init__()  # 初始化基类
        self.title("视频解析助手 @Author: YoungYuan")
        # 设置窗体的宽、高
        window_width = 610
        window_height = 145
        # 获取屏幕宽、高
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # 计算窗口在屏幕上居中的坐标位置
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.resizable(0, 0)
        self.url = tk.StringVar()
        self.v = tk.IntVar()
        self.v.set(1)
        self.frame_1 = tk.Frame(self)
        self.frame_2 = tk.Frame(self)
        self.group = tk.Label(self.frame_1, text="播放通道:")
        self.tb1 = tk.Radiobutton(self.frame_1, text="第一通道",
                                  variable=self.v, value=1, width=10, height=3)
        self.tb2 = tk.Radiobutton(self.frame_1, text="第二通道",
                                  variable=self.v, value=2, width=10, height=3)
        self.tb3 = tk.Radiobutton(self.frame_1, text="第三通道",
                                  variable=self.v, value=3, width=10, height=3)
        self.label = tk.Label(self.frame_2, text="视频播放地址：")
        self.entry = tk.Entry(self.frame_2, textvariable=self.url, width=50)
        self.play = tk.Button(self.frame_2, text="播放", font=("微软雅黑", 12),
                              bg="#9E9D9D", width=12, command=self.video_play)
        self.exit = tk.Button(self.frame_2, text="退出", font=("微软雅黑", 12),
                               bg="#9E9D9D", width=12, command=self.quit)
        # 控件布局之前，需要激活软件空间
        self.frame_1.pack()
        self.frame_2.pack()

        self.group.grid(row=0, column=0)
        self.tb1.grid(row=0, column=1)
        self.tb2.grid(row=0, column=2)
        self.tb3.grid(row=0, column=3)
        self.label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1, columnspan=3)
        self.play.grid(row=1, column=1, padx=10, pady=10)
        self.exit.grid(row=1, column=2, padx=10, pady=10)

    def video_play(self):
        port = {
            1: "https://im1907.top/?jx=",
            2: "https://bd.jx.cn/?url=",
            3: "https://jx.m3u8.tv/jiexi/?url="
            
        }
        key = self.v.get()
        API = port[key]
        if re.match(r'https?:/{2}\w.+$', self.url.get()):
            play_url = self.url.get()
            # 对含有特殊符号的URL进行编码，使其转换为合法的url字符串
            play_url = parse.quote_plus(play_url)
            webbrowser.open(API + play_url)
            self.quit()
        else:
            msgbox.showwarning(title="错误", message="视频地址无效，请重新输入！")


if __name__ == '__main__':
    app = Application()
    app.mainloop()
