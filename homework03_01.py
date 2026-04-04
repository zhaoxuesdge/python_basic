# 解析MAC地址表

import re

mac_table = '166    54a2.74f7.0326    DYNAMIC     Gi1/0/11'
re_result = re.match(r"^(\d{1,4})\s+([0-9a-f]{4}.[0-9a-f]{4}.[0-9a-f]{4})\s+(\S+)\s+([A-Z]\S+\d)",mac_table).groups()

mac_format = "{0:<6}:  {1}\n{2:<6}:  {3}\n{4:<6}:  {5}\n{6:<6}:  {7}\n"
output_format = mac_format.format("VLAN",re_result[0],"MAC",re_result[1],"Type",re_result[2],"Port",re_result[3])

print(output_format)