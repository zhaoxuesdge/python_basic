# 导入random模块，随机产生网络IPv4地址。

import random

ip_address = str(random.randint(1, 255)) + "." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255))
print(ip_address)