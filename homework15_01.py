import datetime

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 创建数据库引擎（SQLite；脚本同级目录生成 device_inventory.db）
engine = create_engine(
    "sqlite:///device_inventory.db?check_same_thread=False",
    echo=False,
)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, index=True)
    type = Column(String(64), nullable=False)
    version = Column(String(64))
    location = Column(String(128))
    # SQLite 存本地时间；入库时由 default 自动填写当前时间
    create_time = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(设备名称: {self.name} | 类型: {self.type} | "
            f"版本: {self.version} | 位置: {self.location} | 入库时间: {self.create_time})"
        )


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    if session.query(Device).count() == 0:
        device_list = [
            {
                "name": "R1",
                "type": "router",
                "version": "IOS XE 17.14",
                "location": "Beijing-IDC-A",
            },
            {
                "name": "R2",
                "type": "router",
                "version": "IOS XE 17.14",
                "location": "Shanghai-IDC-B",
            },
            {
                "name": "SW1",
                "type": "switch",
                "version": "IOS 15.2",
                "location": "Beijing-IDC-A",
            },
            {
                "name": "SW2",
                "type": "switch",
                "version": "IOS 15.2",
                "location": "Shanghai-IDC-B",
            },
            {
                "name": "FW1",
                "type": "firewall",
                "version": "ASA 9.16",
                "location": "Beijing-IDC-A",
            },
            {
                "name": "FW2",
                "type": "firewall",
                "version": "FTD 7.2",
                "location": "Shenzhen-IDC-C",
            },
        ]
        for row in device_list:
            session.add(Device(**row))
        session.commit()
        print("[+] 初始设备数据已写入数据库")

    while True:
        print("\n请输入查询选项:")
        print("输入 1：查询所有设备")
        print("输入 2：根据设备名称查询")
        print("输入 3：根据设备类型查询")
        print("输入 4：根据机房位置查询")
        print("输入 0：退出")

        while True:
            choice = input("\n请输入查询选项：").strip()
            if choice in ("0", "1", "2", "3", "4"):
                break
            print("无效的选项，请重新输入（0-4）")

        if choice == "1":
            results = session.query(Device).all()
            for d in results:
                print(d)

        elif choice == "2":
            name = input("请输入设备名称：")
            results = session.query(Device).filter(Device.name == name).all()
            for d in results:
                print(d)

        elif choice == "3":
            device_type = input("请输入设备类型（router/switch/firewall）：")
            results = session.query(Device).filter(Device.type == device_type).all()
            for d in results:
                print(d)

        elif choice == "4":
            keyword = input("请输入机房位置关键词：")
            results = (
                session.query(Device).filter(Device.location.contains(keyword)).all()
            )
            for d in results:
                print(d)

        elif choice == "0":
            break

    session.close()