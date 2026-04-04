from pythonping import ping
def ping_check(host):
    """
    返回: (is_reachable, rtt_ms)
    is_reachable: True/False
    rtt_ms: float(毫秒) 或 None
    """
    result = ping(host, count=1, timeout=2)
    if result.success():
        # rtt_avg_ms 在 pythonping 中通常可直接取到（单位毫秒）
        return True, result.rtt_avg_ms
    else:
        return False, None
if __name__ == "__main__":
    gateways = ["192.168.50.1", "10.0.0.1", "172.16.1.1"]
    for gw in gateways:
        reachable, rtt = ping_check(gw)
        if reachable:
            print("{:<13}: 可达   | RTT: {:.2f} ms".format(gw, rtt))
        else:
            print("{:<13}: 不可达".format(gw))
