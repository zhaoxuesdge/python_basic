l1 = [100, 1000, 10, 400, 25, 40, 0]

# l2 = l1  # 引用：会导致排序后 l1 也被改变
l2 = l1.copy()  # 拷贝：l1 保持不变
l2.sort()

print("{:<8}{}".format("l1", "l2"))
for a, b in zip(l1, l2):
    print("{:<8}{}".format(a, b))
