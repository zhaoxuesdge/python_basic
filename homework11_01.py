import re

from homework09_01 import ssh_run

SHOW_RUNNING_CONFIG = "show running-config"


def _extract_hostname_to_end(raw: str) -> str:
    """使用正则一次性提取 hostname 到 end 之间的全部内容。"""
    m = re.search(r"(hostname[\s\S]+end)", raw)
    if not m:
        return ""
    return m.group(1)


def get_cisco_running_config(host: str, username: str, password: str) -> str:
    """
    复用 homework09_01 的 ssh_run，SSH 登录思科设备执行 show running-config，
    只返回 hostname 到 end 之间的有效配置字符串。
    若输出被分页截断，请在设备 line vty 上配置 length 0。
    """
    output = ssh_run(host, username, password, SHOW_RUNNING_CONFIG)
    return _extract_hostname_to_end(output)


if __name__ == "__main__":
    # 按你的思科路由器修改以下三项后运行测试
    ROUTER_HOST = "10.10.1.254"
    USERNAME = "cisco"
    PASSWORD = "Cisc0123"

    config = get_cisco_running_config(ROUTER_HOST, USERNAME, PASSWORD)
    print(config if config else "(未截取到 hostname～end 段落，请检查 SSH 输出是否完整)")
