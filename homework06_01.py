# 解析 ASA 防火墙连接表为字典（支持任意多行）

import re

asa_conn = (
    "TCP Student 192.168.189.167:32806 Teacher 137.78.5.128:65247, idle 0:00:00, bytes 74, flags UIO\n"
    "TCP Student 192.168.189.167:80 Teacher 137.78.5.128:65233, idle 0:00:03, bytes 334516, flags UIO"
)

# 每行: TCP Student 源IP:源端口 Teacher 目的IP:目的端口, ... bytes N, flags XXX
_LINE_RE = re.compile(
    r"^TCP\s+Student\s+"
    r"(?P<src_ip>\d{1,3}(?:\.\d{1,3}){3}):(?P<src_port>\d+)\s+"
    r"Teacher\s+"
    r"(?P<dst_ip>\d{1,3}(?:\.\d{1,3}){3}):(?P<dst_port>\d+)"
    r".*?bytes\s+(?P<bytes>\d+),\s*flags\s+(?P<flags>\S+)",
    re.DOTALL,
)

conn_dict = {}
for raw_line in asa_conn.split("\n"):
    line = raw_line.strip()
    if not line:
        continue
    m = _LINE_RE.match(line)
    if not m:
        continue
    g = m.groupdict()
    key = (g["src_ip"], g["src_port"], g["dst_ip"], g["dst_port"])
    conn_dict[key] = (g["bytes"], g["flags"])

print(conn_dict)

sep = "=" * 84
W_LABEL = 10
W_VAL1 = 17
W_VAL2 = 6

for key, val in conn_dict.items():
    src_ip, src_port, dst_ip, dst_port = key
    bytes_s, flags_s = val
    print(
        "{:<{lw}}: {:<{vw1}} | {:<{lw}}: {:<{vw2}} | {:<{lw}}: {:<{vw1}} | {:<{lw}}: {}".format(
            "src",
            src_ip,
            "src_port",
            src_port,
            "dst",
            dst_ip,
            "dst_port",
            dst_port,
            lw=W_LABEL,
            vw1=W_VAL1,
            vw2=W_VAL2,
        )
    )
    print(
        "{:<{lw}}: {:<{vw1}} | {:<{lw}}: {}".format(
            "bytes",
            bytes_s,
            "flags",
            flags_s,
            lw=W_LABEL,
            vw1=W_VAL1,
        )
    )
    print(sep)
