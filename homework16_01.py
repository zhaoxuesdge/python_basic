import sys
import os
import hashlib
import time
import datetime
import re

# ---- 1. 复用第12天的 qytang_multicmd ----
# 确保路径正确以导入之前的模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from homework12_01 import qytang_multicmd  # noqa: E402
except ImportError:
    print("错误：无法找到 homework12_01.py，请检查路径。")
    sys.exit(1)

# ---- 2. SQLAlchemy ORM ----
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///router_config.db',
                       connect_args={'check_same_thread': False})
Base = declarative_base()
Session = sessionmaker(bind=engine)

class RouterConfig(Base):
    """路由器配置备份模型"""
    __tablename__ = 'router_config'
    id            = Column(Integer, primary_key=True)
    router_ip     = Column(String(64),   nullable=False, index=True)
    router_config = Column(String(99999), nullable=False)
    config_hash   = Column(String(500),   nullable=False)
    record_time   = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"路由器IP地址: {self.router_ip} | "
                f"配置Hash: {self.config_hash} | "
                f"记录时间: {self.record_time})")

# 创建表
Base.metadata.create_all(engine, checkfirst=True)

# ---- 3. 工具函数 ----
def get_show_run(host, username, password):
    """获取配置并计算 hash"""
    raw = qytang_multicmd(host, username, password,
                          ['terminal length 0', 'show running-config'],
                          verbose=False)
    
    # 使用正则匹配配置核心部分 (从 hostname 开始到 end 结束)
    match = re.search(r'(hostname[\s\S]+end)', raw)
    if match:
        config = match.group(1) # 从 match 中取出配置文本
    else:
        config = raw # 如果匹配不到，回退到原始输出
        
    # 对配置文本做 SHA256 (注意必须 encode 为 bytes)
    config_hash = hashlib.sha256(config.encode('utf-8')).hexdigest()
    return config, config_hash

def save_config(host, config, config_hash):
    """写入数据库（使用独立 session，避免事务残留）"""
    with Session() as session:
        record = RouterConfig(
            router_ip=host, 
            router_config=config, 
            config_hash=config_hash
        )
        session.add(record)
        session.commit()

def get_latest_two_hashes(host):
    """查询最近两条记录"""
    with Session() as session:
        results = (session.query(RouterConfig)
                   .filter(RouterConfig.router_ip == host) # 按 router_ip 过滤
                   .order_by(RouterConfig.id.desc())
                   .limit(2)
                   .all())
        return results

# ---- 4. 主循环 ----
if __name__ == '__main__':
    # 配置信息（请根据实际情况修改）
    host     = '10.10.1.254'
    username = 'cisco'
    password = 'Cisc0123'

    print(f"[*] 开始监控 {host} 的配置变化，每 5 秒采集一次...\n")
    
    try:
        while True:
            # 1. 采集并计算
            config, config_hash = get_show_run(host, username, password)
            
            # 2. 存入数据库
            save_config(host, config, config_hash)
            
            # 3. 获取最近两条进行比对
            records = get_latest_two_hashes(host)

            if len(records) < 2:
                # 第一条记录时，直接打印 hash
                print(f"本次采集的HASH:{config_hash}")
            elif records[0].config_hash == records[1].config_hash:
                # 配置无变化，打印本次 hash
                print(f"本次采集的HASH:{config_hash}")
            else:
                # 配置有变化，打印告警及前后两次 hash
                print("==========配置发生变化==========")
                print(f"  THE MOST RECENT HASH  {records[0].config_hash}")
                print(f"  THE LAST HASH         {records[1].config_hash}")
            
            # 4. 等待 5 秒
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n[*] 监控已由用户停止。")