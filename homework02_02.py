# 切片：提取接口类型和编号

interface = "GigabitEthernet0/0/1"
interface_type = interface[:15]
interface_number = interface[15:]

print(f"接口类型：{interface_type}")
print(f"接口编号：{interface_number}")