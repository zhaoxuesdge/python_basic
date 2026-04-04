import os

route_n_result = os.popen("route -n").read()

gateway = None
for line in route_n_result.splitlines():
    parts = line.split()
    if len(parts) < 4:
        continue
    destination, gw, _genmask, flags = parts[0], parts[1], parts[2], parts[3]
    if destination == "0.0.0.0" and "UG" in flags:
        gateway = gw
        break

print(route_n_result)
print("网关为: {}".format(gateway))