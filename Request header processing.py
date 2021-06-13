# -*- coding: UTF-8 -*-
# @Time: 2020/11/15 18:24
# @Author: YoungYuan

import re

old_headers = '''
Accept: image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cache-Control: no-cache
Connection: keep-alive


'''

pattern = r'^(.*?):[\s]*(.*?)$'
repl = r"'\1': '\2',"
headers = ""

for line in old_headers.splitlines():
    headers += (re.sub(pattern, repl, line)) + '\n'

print(headers[:-2])
