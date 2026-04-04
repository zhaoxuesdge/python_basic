# f-string：打印一条Syslog告警

date = "2026-03-03"
hostname = "SW-Core-01"
level = "CRITICAL"
message = "%LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to down"

print(f"{date} {hostname} {level} {message}")