# 解析ifconfig并ping网关

import os
import re

result = os.popen("ifconfig ens160").read()

# 解析 ifconfig

re_result = re.search(
    r"inet\s+(?P<ip>(?:\d{1,3}\.){3}\d{1,3})\s+netmask\s+(?P<netmask>(?:\d{1,3}\.){3}\d{1,3})\s+broadcast\s+(?P<broadcast>(?:\d{1,3}\.){3}\d{1,3})"
    r"[\s\S]*?\bether\s+(?P<mac>(?:[0-9a-f]{2}:){5}[0-9a-f]{2})",
    result,
    flags=re.IGNORECASE,
).groups()

re_format = "{0:<10}:  {1}\n{2:<10}:  {3}\n{4:<10}:  {5}\n{6:<10}:  {7}"
output_format = re_format.format("IP",re_result[0],"Netmask",re_result[1],"Broadcast",re_result[2],"MAC",re_result[3])

print(output_format)

# ping 网关

str_ip = re_result[0].split(".")
str_ip[3] = str(1)
str_gw = '.'.join(str_ip)

command = f"ping -c 4 {str_gw}"

with os.popen(command) as pipe:
    response = pipe.read()

print(response)