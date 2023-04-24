# -*- encoding: utf-8 -*-
'''
@File    :   Aria2_BT_track.py
@Time    :   2022/08/27 14:08:29
@Author  :   YoungYuan 
@Contact :   young_yuan@hotmail.com
@License :   (C)Copyright 2022-2031, YoungYuan
'''


import re
import requests
from faker import Faker


def get_tracker(url):
    ua = Faker().chrome()

    respones = requests.get(url, headers={"user-agent": ua})
    # 返回码304代表服务端已经执行了GET，但文件未变化；返回码200代表正常的服务器内容
    if respones.status_code == 304 or respones.status_code == 200:
        result = re.sub(r"\n[\s| ]*\n", ',', respones.text)

        return result

    else:
        return False


def update_tracker(new_tracker):
    path = "/Users/youngyuan/.config/aria2/aria2.conf"
    with open(path, mode="r+", encoding="utf-8") as f:
        config_text = f.read()
        old_tracker = re.findall(r"bt-tracker=(.*)", config_text)[0]
        config_text = re.sub(old_tracker, new_tracker, config_text)

        f.seek(0)  # f.read()以后，指针在文本最后，需要回到文本起始位置
        f.truncate()  # 截断，起始位置以后的内容被删除
        f.write(config_text)

    print(f"配置文件 {path} 已完成更新！")


if __name__ == "__main__":
    tracker_url = "https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/best_aria2.txt"
    tracker_result = get_tracker(tracker_url)
    if tracker_result:
        update_tracker(tracker_result)
    else:
        print("无法获取Tracker的相关信息！")
