import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from homework08_02 import ping_check
from homework09_01 import ssh_run

SHOW_IP_INT_BRIEF = "show ip interface brief"


def collect_cisco_interfaces(hosts, username, password, command=SHOW_IP_INT_BRIEF):
    """
    对多个 IP 先 ping，可达则 SSH 采集接口信息并打印；不可达则跳过。
    """
    for ip in hosts:
        reachable, _rtt = ping_check(ip)
        if not reachable:
            print(f"[x] {ip} 不可达，跳过")
            continue
        print(f"[*] {ip} 可达，正在采集...")
        try:
            out = ssh_run(ip, username, password, command)
        except Exception as e:
            print(f"[!] {ip} SSH 失败: {e}")
            continue
        print(f"---------- {ip} 接口信息 ----------")
        print(out.rstrip("\n"))
        print()


if __name__ == "__main__":
    # 思科路由器：按实际环境修改 IP / 账号
    ROUTERS = ["10.10.1.254", "10.10.1.253","10.10.1.252"]
    USERNAME = "cisco"
    PASSWORD = "Cisc0123"

    collect_cisco_interfaces(ROUTERS, USERNAME, PASSWORD)
