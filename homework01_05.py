# 打印IP规划表

Device1 = ["CoreSwitch\t", "10.1.1.1\t", "核心交换机"]
Device2 = ["Firewall\t", "10.1.1.2\t", "防火墙"]
Device3 = ["WLC\t\t", "10.1.1.3\t", "无线控制器"]

print("="*14 + " IP地址规划表 " + "="*14)
print("设备名称\t管理地址\t角色")
print("-"*42)
print(Device1[0] + Device1[1] + Device1[2])
print(Device2[0] + Device2[1] + Device2[2])
print(Device3[0] + Device3[1] + Device3[2])
print("="*42)