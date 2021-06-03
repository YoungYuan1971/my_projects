# -*- coding: UTF-8 -*-
# @Time: 2020/11/15 18:24
# @Author: YoungYuan

import re

old_headers = '''



'''

pattern = '^(.*?):[\s]*(.*?)$'
headers = ""
for line in old_headers.splitlines():
    headers += (re.sub(pattern, '\'\\1\': \'\\2\',', line)) + '\n'
print(headers[:-2])
