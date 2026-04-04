import os
import re
import time

while True:
    output = os.popen("ss -tulnp").read()
    lines = output.splitlines()
    tcp80_listening = False
    for line in lines:
        line_lower = line.lower()
        if re.search(r"\btcp\b", line_lower) and re.search(r":80(\s|$)", line):
            if "listen" in line_lower:
                tcp80_listening = True
                break
    if tcp80_listening:
        print("[!] 告警: TCP/80 已开放！请检查是否为授权服务。")
        break
    else:
        print("[*] 检测中... TCP/80 未监听")
        time.sleep(1)
