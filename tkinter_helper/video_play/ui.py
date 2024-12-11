"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
import random
from tkinter import *
from tkinter.ttk import *


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_label_channel = self.__tk_label_channel(self)
        self.tk_label_play_url = self.__tk_label_play_url(self)
        self.tk_radio_button_channel_one = self.__tk_radio_button_channel_one(
            self)
        self.tk_radio_button_channel_two = self.__tk_radio_button_channel_two(
            self)
        self.tk_radio_button_channel_three = self.__tk_radio_button_channel_three(
            self)
        self.tk_input_play_url = self.__tk_input_play_url(self)
        self.tk_button_play = self.__tk_button_play(self)
        self.tk_button_destroy = self.__tk_button_destroy(self)

    def __win(self):
        self.title("视频解析助手 @Author: YoungYuan")
        # 设置窗口大小、居中
        width = 612
        height = 146
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar:
                vbar.lift(widget)
            if hbar:
                hbar.lift(widget)

        def hide():
            if vbar:
                vbar.lower(widget)
            if hbar:
                hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar:
            vbar.bind("<Enter>", lambda e: show())
        if vbar:
            vbar.bind("<Leave>", lambda e: hide())
        if hbar:
            hbar.bind("<Enter>", lambda e: show())
        if hbar:
            hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph,
                   relheight=h / ph, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph,
                   relwidth=w / pw, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_label_channel(self, parent):
        label = Label(parent, text="播放通道：", anchor="center", )
        label.place(x=142, y=16, width=67, height=30)
        return label

    def __tk_label_play_url(self, parent):
        label = Label(parent, text="视频播放地址：", anchor="center", )
        label.place(x=33, y=53, width=88, height=30)
        return label

    def __tk_radio_button_channel_one(self, parent):
        rb = Radiobutton(parent, text="第一通道",)
        rb.place(x=212, y=16, width=80, height=30)
        return rb

    def __tk_radio_button_channel_two(self, parent):
        rb = Radiobutton(parent, text="第二通道",)
        rb.place(x=300, y=16, width=80, height=30)
        return rb

    def __tk_radio_button_channel_three(self, parent):
        rb = Radiobutton(parent, text="第三通道",)
        rb.place(x=388, y=16, width=80, height=30)
        return rb

    def __tk_input_play_url(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=124, y=53, width=453, height=30)
        return ipt

    def __tk_button_play(self, parent):
        btn = Button(parent, text="播放", takefocus=False,)
        btn.place(x=153, y=95, width=115, height=30)
        return btn

    def __tk_button_destroy(self, parent):
        btn = Button(parent, text="退出", takefocus=False,)
        btn.place(x=370, y=95, width=115, height=30)
        return btn


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)

    def __event_bind(self):
        self.tk_button_play.bind('<Button-1>', self.ctl.play_video)
        self.tk_button_destroy.bind('<Button-1>', self.ctl.destroy)
        pass

    def __style_config(self):
        pass


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
