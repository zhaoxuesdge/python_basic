import os
import shutil
files = {
    "R1_config.txt": "hostname R1\ninterface GigabitEthernet0/0\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n",
    "R2_config.txt": "hostname R2\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n",
    "R3_config.txt": "hostname R3\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n",
    "SW1_config.txt": "hostname SW1\ninterface Vlan1\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n",
}
backup_dir = "backup"
# 1) 创建目录并写入文件
os.makedirs(backup_dir, exist_ok=True)
for filename, content in files.items():
    path = os.path.join(backup_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
# 2) 遍历目录，找出含有 shutdown（排除 no shutdown）的文件名
matches = []
for filename in os.listdir(backup_dir):
    path = os.path.join(backup_dir, filename)
    if not os.path.isfile(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    found = False
    for line in content.splitlines():
        if line.strip() == "shutdown":   # 精确匹配 shutdown 行（自然排除了 no shutdown）
            found = True
            break
    if found:
        matches.append(filename)
print("发现包含 shutdown 接口的设备配置文件:")
for name in matches:
    print(name)
# 3) 删除 backup/ 目录及其所有文件
shutil.rmtree(backup_dir)
print("backup/ 目录已清理")