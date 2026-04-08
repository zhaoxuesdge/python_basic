import time

import paramiko


def qytang_multicmd(
    ip, username, password, cmd_list, enable="", wait_time=2, verbose=True
):
    """
    参数说明：
      cmd_list  : 要执行的命令列表，例如 ['terminal length 0', 'show version']
      enable    : enable 密码，若设备无需 enable 则保持默认空字符串
      wait_time : 每条命令发送后等待设备响应的秒数
      verbose   : True 则打印每条命令的返回结果，False 则静默执行
    返回值：
      dict，key 为命令，value 为命令返回文本
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        ip,
        port=22,
        username=username,
        password=password,
        timeout=5,
        look_for_keys=False,
        allow_agent=False,
    )

    chan = ssh.invoke_shell()
    outputs = {}

    try:
        # 读取初始登录提示符
        time.sleep(1)
        _ = chan.recv(65535).decode("utf-8", errors="ignore")

        # 如需进入特权模式，先执行 enable
        if enable:
            chan.send("enable\n")
            time.sleep(wait_time)
            _ = chan.recv(65535).decode("utf-8", errors="ignore")
            chan.send(f"{enable}\n")
            time.sleep(wait_time)
            _ = chan.recv(65535).decode("utf-8", errors="ignore")

        for cmd in cmd_list:
            chan.send(f"{cmd}\n")
            time.sleep(wait_time)
            output = chan.recv(65535).decode("utf-8", errors="ignore")
            outputs[cmd] = output

            if verbose:
                print(f"--- {cmd} ---")
                print(output.rstrip())
                print()
    finally:
        ssh.close()

    return outputs


if __name__ == "__main__":
    ip = "10.10.1.254"
    username = "cisco"
    password = "Cisc0123"

    cmd_list = [
        "terminal length 0",
        "show version",
        "config ter",
        "router ospf 1",
        "network 10.0.0.0 0.0.0.255 area 0",
        "end",
    ]

    qytang_multicmd(ip, username, password, cmd_list, enable="", wait_time=2, verbose=True)
