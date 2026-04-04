# 使用 format() 打印一份格式整齐的接口状态报告

intf1 = "Gi0/0"
intf2 = "Gi0/1"
intf3 = "Gi0/2"
status1 = "up"
status2 = "down"
status3 = "up"
speed1 = "1G"
speed2 = "1G"
speed3 = "10G"

title = "{0:<18}{1:<18}{2}"
inspect = "{interface:<20}{status:<20}{speed:<}"
print(title.format("接口","状态","速率"))
print("-" * 45)
print(inspect.format(interface = intf1,status = status1,speed = speed1))
print(inspect.format(interface = intf2,status = status2,speed = speed2))
print(inspect.format(interface = intf3,status = status3,speed = speed3))