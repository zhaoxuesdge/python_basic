import os
import time
from datetime import datetime, timedelta


def main():
    # 1. 确定备份目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(base_dir, "backup")

    # 如果目录不存在则创建
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    print(f"开始模拟备份，目录: {backup_dir}")
    print("按 Ctrl+C 停止并清理...")

    try:
        while True:
            # 2. 获取当前时间并生成备份文件
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"backup_{now_str}.txt"
            filepath = os.path.join(backup_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"backup at {now_str}\n")

            print(f"\n[+] 创建备份: {filename}")

            # 3. 计算 15 秒前的时间基准（早于此时间的备份视为过期）
            expire_time = now - timedelta(seconds=15)

            # 4. 遍历备份目录，找出过期文件并删除
            current_files = []
            for file in os.listdir(backup_dir):
                if not (file.startswith("backup_") and file.endswith(".txt")):
                    continue
                time_str = file.replace("backup_", "").replace(".txt", "")
                try:
                    file_time = datetime.strptime(time_str, "%Y-%m-%d_%H-%M-%S")
                except ValueError:
                    continue

                fullpath = os.path.join(backup_dir, file)
                if file_time < expire_time:
                    os.remove(fullpath)
                    print(f"[-] 删除过期: {file}")
                else:
                    current_files.append(file)

            # 5. 打印当前保留的所有备份文件
            print(f"[*] 当前保留的备份 ({len(current_files)}个):")
            for f in sorted(current_files):
                print(f"    - {f}")

            # 6. 休眠 3 秒
            time.sleep(3)

    except KeyboardInterrupt:
        print("\n\n收到停止信号，正在清理所有备份文件...")
        if os.path.isdir(backup_dir):
            for file in os.listdir(backup_dir):
                if file.startswith("backup_") and file.endswith(".txt"):
                    fp = os.path.join(backup_dir, file)
                    if os.path.isfile(fp):
                        os.remove(fp)
                        print(f"[-] 已清理: {file}")
            try:
                os.rmdir(backup_dir)
                print("[-] 已删除 backup 目录")
            except OSError:
                pass
        print("清理完成，程序退出。")


if __name__ == "__main__":
    main()
