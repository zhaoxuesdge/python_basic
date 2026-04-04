import re
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
if __name__ == "__main__":
    host = "10.10.1.205"
    username = "root"
    password = "Ting38167261()"
    route_output = ssh_run(host, username, password, "route -n")
    default_gw = None
    for line in route_output.splitlines():
        # route -n 典型格式:
        # Destination  Gateway      Genmask         Flags Metric Ref Use Iface
        # 0.0.0.0      196.21.5.1   0.0.0.0         UG    ...
        m = re.match(
            r"^\s*0\.0\.0\.0\s+(\d{1,3}(?:\.\d{1,3}){3})\s+\S+\s+(\S+)\b",
            line
        )
        if m:
            gateway = m.group(1)
            flags = m.group(2)
            if "UG" in flags:
                default_gw = gateway
                break
    if default_gw:
        print(f"默认网关: {default_gw}")
    else:
        print("未找到默认网关")