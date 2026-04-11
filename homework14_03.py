"""
任务三：使用 PyInstaller 将「任务二」SSH 命令行脚本打包为独立可执行程序

重要：
  - 必须在 Windows 下打包，才能生成 .exe（与操作系统绑定）。
  - 本仓库中任务二脚本文件名为 homework14_02.py（对应教材中的 day14_task02_ssh_argparse.py）。

前置（在 Windows 上，建议先进入项目目录）：
  pip install pyinstaller paramiko cryptography bcrypt

在 PowerShell 中执行打包（反引号 ` 为 PowerShell 换行续行）：

  pyinstaller --onefile `
    --hidden-import=paramiko `
    --hidden-import=cryptography `
    --hidden-import=cryptography.hazmat.primitives.asymmetric.ed25519 `
    --hidden-import=cryptography.hazmat.backends.openssl `
    --hidden-import=bcrypt `
    homework14_02.py

打包完成后，在 dist\\ 目录下会得到 homework14_02.exe，测试示例：

  .\\dist\\homework14_02.exe -i 196.21.5.211 -u admin -p Cisc0123 -c "show ip inter brief"

说明：paramiko 依赖较多加密相关模块，若运行时仍报缺模块，可再按需增加 --hidden-import=模块名。
"""

import re
import argparse
import os
import sys
import paramiko

def ssh_run(host, username, password, command):
    """
    SSH 执行命令并返回输出字符串
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=host,
        username=username,
        password=password,
        look_for_keys=False,   # 禁用本地密钥查找
        allow_agent=False      # 禁用 SSH agent
    )
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode("utf-8", errors="ignore")
    err = stderr.read().decode("utf-8", errors="ignore")
    client.close()
    # 如有错误输出，可按需处理；这里简单拼接返回，避免丢失信息
    return output if output.strip() else err

def main():
    parser = argparse.ArgumentParser(description="网络设备 SSH 命令执行工具")

    parser.add_argument("-i", "--ip", required=True, help="设备的 IP 地址")
    parser.add_argument("-u", "--username", required=True, help="登录用户名")
    parser.add_argument("-p", "--password", required=True, help="登录密码")
    parser.add_argument("-c", "--cmd", required=True, help="要执行的命令")

    args = parser.parse_args()

    result = ssh_run(args.ip, args.username, args.password, args.cmd)
    print(result.rstrip("\n"))


if __name__ == "__main__":
    main()

"""	
pyinstaller --onefile `
  --hidden-import=paramiko `
  --hidden-import=cryptography `
  --hidden-import=cryptography.hazmat.primitives.asymmetric.ed25519 `
  --hidden-import=cryptography.hazmat.backends.openssl `
  --hidden-import=bcrypt `
  homework14_03.py
  .\\dist\\homework14_03.exe -i 10.10.1.254 -u cisco -p Cisc0123 -c "show ip inter brief"

"""	