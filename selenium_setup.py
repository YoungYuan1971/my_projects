# -*- coding: UTF-8 -*-
# @Time: 2020/11/8 20:51
# @Author: YoungYuan

# 下述一段js也可以规避检测
'''
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
"source": """
Object.defineProperty(navigator, 'webdriver', {
get: () => undefined
})
"""
})
'''


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep


class BrowserSetup:
    def __init__(self):
        self.cookies_lst = []
        # 设置chromedriver可执行路径，如果是环境变量，则无需设置
        # self.service = Service(
        #     executable_path='chromedriver')
        # 设置规避网站检测
        self.option = Options()
        self.option.add_argument(
            "--disable-blink-features=AutomationControlled")
        # 阻止浏览器自动关闭
        self.option.add_experimental_option("detach", True)

    def without_header(self):
        # 设置无头浏览器，即无可视化界面的操作
        self.option.add_argument('--headless')
        self.option.add_argument('--disable-gpu')
        # 创建浏览器对象
        web = webdriver.Chrome(options=self.option)
        web.implicitly_wait(10)  # 设置隐式等待时间
        return web

    def with_header(self):
        web = webdriver.Chrome(options=self.option)
        web.implicitly_wait(10)  # 设置隐式等待时间
        return web

    def web(self, visible: bool = True):
        if visible:
            return self.with_header()
        else:
            return self.without_header()

    def get_cookies(self, cookies_lst: list):
        self.cookies_lst = cookies_lst
        cookies_dic = {}
        for cookie in self.cookies_lst:
            cookies_dic[cookie['name']] = cookie['value']

        return cookies_dic


if __name__ == '__main__':
    url = "https://www.baidu.com"

    app = BrowserSetup()
    with app.web(visible=True) as chrome:
        chrome.maximize_window()
        chrome.implicitly_wait(10)

        chrome.get(url)
        cookies_list = chrome.get_cookies()
        cookies = app.get_cookies(cookies_lst=cookies_list)
        print(cookies)
        sleep(5)
