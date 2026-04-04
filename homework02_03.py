# 处理show version输出

version_raw = "  Cisco IOS XE Software, Version 17.03.04  "

print(version_raw.strip())
print(version_raw.strip().upper())
print(version_raw.strip().replace("17.03.04", "17.06.01"))