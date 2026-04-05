import hashlib
import sys
import time

from homework11_01 import get_cisco_running_config


def config_md5(config: str) -> str:
    """对配置字符串计算 MD5 十六进制摘要。"""
    return hashlib.md5(config.encode("utf-8")).hexdigest()


def watch_config_md5(host: str, username: str, password: str, interval: float = 5.0) -> None:
    """
    函数二：每 interval 秒调用 homework11_01.get_cisco_running_config 获取配置并计算 MD5；
    与上一次相同则打印当前 MD5；不同则打印告警并退出。
    """
    prev_md5 = None
    while True:
        config = get_cisco_running_config(host, username, password)
        digest = config_md5(config)

        if prev_md5 is not None and digest != prev_md5:
            print(f"[!] 告警: 配置已改变！新 MD5: {digest}")
            sys.exit(0)

        print(f"[*] 当前配置 MD5: {digest}")
        prev_md5 = digest
        time.sleep(interval)


if __name__ == "__main__":
    ROUTER_HOST = "10.10.1.254"
    USERNAME = "cisco"
    PASSWORD = "Cisc0123"

    watch_config_md5(ROUTER_HOST, USERNAME, PASSWORD)
