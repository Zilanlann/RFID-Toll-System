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
    CREATE TABLE IF NOT EXISTS VehicleInfo (
        VehicleID INT AUTO_INCREMENT PRIMARY KEY,
        LicensePlate VARCHAR(20) NOT NULL,
        VehicleType VARCHAR(50),
        OwnerName VARCHAR(100),
        ContactInfo VARCHAR(100)
    )
    """
    create_rfid_tags = """
    CREATE TABLE IF NOT EXISTS RFIDTags (
        TagID INT AUTO_INCREMENT PRIMARY KEY,
        TagNumber VARCHAR(50) NOT NULL,
        VehicleID INT,
        IsActive TINYINT(1) DEFAULT 1,
        FOREIGN KEY (VehicleID) REFERENCES VehicleInfo(VehicleID)
    );
    """
    create_charge_records = """
    CREATE TABLE IF NOT EXISTS ChargeRecords (
        RecordID INT AUTO_INCREMENT PRIMARY KEY,
        VehicleID INT,
        RFIDTagID INT,
        EntryTime DATETIME,
        ExitTime DATETIME,
        Charge DECIMAL(10, 2),
        FOREIGN KEY (VehicleID) REFERENCES VehicleInfo(VehicleID),
        FOREIGN KEY (RFIDTagID) REFERENCES RFIDTags(TagID)
    );
    """
    cursor.execute(create_vehicle_info)
    cursor.execute(create_charge_records)
    cursor.execute(create_rfid_tags)


def add_new_car(car: str, card_id: str):
    """添加一条车辆数据以及关联的RFIDTag"""
    insert_data_query = """
    INSERT INTO VehicleInfo (LicensePlate)
    VALUES ('%s')
    """ % car
    vehicle_id = cursor.execute("SELECT * FROM VehicleInfo where LicensePlate=%s", car)
    insert_rfid = """
    INSERT INTO RFIDTags (TagNumber, VehicleID)
    VALUES ('%s', '%s')
    """ % (card_id, vehicle_id)
    cursor.execute(insert_data_query)
    cursor.execute(insert_rfid)
    db.commit()


def delete_all():
    cursor.execute("DROP TABLE IF EXISTS ChargeRecords, VehicleInfo, RFIDTags;")
