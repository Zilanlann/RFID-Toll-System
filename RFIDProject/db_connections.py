from datetime import datetime

import pymysql

db = pymysql.connect(
    host="localhost",
    db="mysql",
    user="root",
    password="kiwMmya7xtS%DE"
)
cursor = db.cursor()


def init_table():
    """初始化VehicleInfo, ChargeRecords, RFIDTags表"""
    create_vehicle_info = """
    CREATE TABLE IF NOT EXISTS vehicle_info (
        VehicleID INT AUTO_INCREMENT PRIMARY KEY,
        LicensePlate VARCHAR(20) NOT NULL,
        VehicleType VARCHAR(50),
        OwnerName VARCHAR(100),
        ContactInfo VARCHAR(100)
    )
    """
    create_rfid_tags = """
    CREATE TABLE IF NOT EXISTS rfid_tags (
        TagID INT AUTO_INCREMENT PRIMARY KEY,
        TagNumber VARCHAR(50) NOT NULL,
        VehicleID INT,
        IsActive TINYINT(1) DEFAULT 1,
        FOREIGN KEY (VehicleID) REFERENCES vehicle_info(VehicleID)
    );
    """
    create_charge_records = """
    CREATE TABLE IF NOT EXISTS charge_records (
        RecordID INT AUTO_INCREMENT PRIMARY KEY,
        VehicleID INT,
        RFIDTagID INT,
        EntryTime DATETIME,
        ExitTime DATETIME,
        Charge DECIMAL(10, 2),
        FOREIGN KEY (VehicleID) REFERENCES vehicle_info(VehicleID),
        FOREIGN KEY (RFIDTagID) REFERENCES rfid_tags(TagID)
    );
    """
    cursor.execute(create_vehicle_info)
    cursor.execute(create_rfid_tags)
    cursor.execute(create_charge_records)


def add_new_car(car: str, card_id: str):
    """添加一条车辆数据以及关联的RFIDTag"""
    try:
        # 插入车辆数据
        insert_data_query = "INSERT INTO vehicle_info (LicensePlate) VALUES (%s)"
        cursor.execute(insert_data_query, car)
        db.commit()  # 提交事务

        # 获取插入后的车辆ID
        cursor.execute("select LAST_INSERT_ID()")
        vehicle_id = cursor.fetchone()[0]

        # 插入RFID标签数据
        insert_rfid = "INSERT INTO rfid_tags (TagNumber, VehicleID) VALUES (%s, %s)"
        cursor.execute(insert_rfid, (card_id, vehicle_id))
        db.commit()
    except Exception as e:
        db.rollback()  # 发生异常时回滚事务
        print(f"An error occurred: {e}")


def car_entry(tag_number):
    """车辆进入停车场"""
    try:
        # 查找与标签号相关的车辆和RFID标签ID
        cursor.execute("SELECT VehicleID, TagID AS RFIDTagID FROM rfid_tags WHERE TagNumber = %s", tag_number)
        (vehicle_id, rfid_tag_id) = cursor.fetchone()

        # 获取当前时间并截取到秒
        entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 记录车辆进入时间
        insert_entry_time_query = "INSERT INTO charge_records (VehicleID, RFIDTagID, EntryTime) VALUES (%s, %s, %s)"
        cursor.execute(insert_entry_time_query, (vehicle_id, rfid_tag_id, entry_time))
        db.commit()  # 提交事务
    except Exception as e:
        db.rollback()  # 发生异常时回滚事务
        print(f"An error occurred: {e}")


def car_exit(tag_number):
    try:
        # 查找与标签号相关的车辆和RFID标签ID
        cursor.execute("SELECT VehicleID, TagID AS RFIDTagID FROM rfid_tags WHERE TagNumber = %s", tag_number)
        (vehicle_id, rfid_tag_id) = cursor.fetchone()

        # 获取当前时间并截取到秒作为离开时间
        exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 查询入场时间
        cursor.execute("SELECT EntryTime FROM charge_records WHERE RFIDTagID = %s AND ExitTime IS NULL", rfid_tag_id)
        entry_time = cursor.fetchone()[0]

        # 计算费用（费率为每小时 X 元）
        hourly_rate = 10  # 费率为 10 元/小时
        exit_time = datetime.strptime(exit_time, '%Y-%m-%d %H:%M:%S')
        time_difference = exit_time - entry_time
        hours = time_difference.total_seconds()
        charge = hours * hourly_rate / 3600
        print(charge)

        # 更新离开时间和费用
        update_query = "UPDATE charge_records SET ExitTime = %s, Charge = %s WHERE RFIDTagID = %s AND ExitTime IS NULL"
        cursor.execute(update_query, (exit_time, charge, rfid_tag_id))
        db.commit()  # 提交事务

    except Exception as e:
        db.rollback()  # 发生异常时回滚事务
        print(f"An error occurred: {e}")


def delete_all():
    cursor.execute("DROP TABLE IF EXISTS charge_records, vehicle_info, rfid_tags")
