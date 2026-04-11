import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from homework09_01 import ssh_run


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
