# 解析ASA防火墙连接表

import re

conn = 'TCP server  172.16.1.101:443 localserver  172.16.66.1:53710, idle 0:01:09, bytes 27575949, flags UIO'

re_result = re.match(r"([A-Z]{1,})\s+\S+\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):(\d{1,})\s+\S+\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):(\d{1,})[\s\S]+",conn).groups()

re_format = "{0:<15}:  {1}\n{2:<15}:  {3}\n{4:<15}:  {5}\n{6:<15}:  {7}\n{8:<15}:  {9}\n"

output_format = re_format.format("Protocol",re_result[0],"Server IP",re_result[1],"Server Port",re_result[2],"Client IP",re_result[3],"Client Port",re_result[4])

print(output_format)