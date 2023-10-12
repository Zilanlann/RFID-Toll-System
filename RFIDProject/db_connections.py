import pymysql

db = pymysql.connect(
    host="localhost",
    db="mysql",
    user="root",
    password="kiwMmya7xtS%DE"
)
cursor = db.cursor()


def init_table():
    """初始化toll_system表"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS toll_system (
        id INT AUTO_INCREMENT PRIMARY KEY,
        car VARCHAR(20) NOT NULL,
        card_id VARCHAR(20) NOT NULL
    )
    """
    cursor.execute(create_table_query)


def add_new_car(car: str, card_id: str):
    insert_data_query = """
    INSERT INTO toll_system (car, card_id)
    VALUES ('%s', '%s')
    """ % (car, card_id)
    cursor.execute(insert_data_query)
    db.commit()


def check_car_exists(quest: str):
    # 执行查询
    cursor.execute("SELECT * FROM toll_system WHERE car=%s", quest)
    result = cursor.fetchone()
    # 返回查询结果
    return result is not None


def delete_datas():
    """删除所有数据"""
    delete_data_query = "DELETE FROM toll_system"
    cursor.execute(delete_data_query)
    db.commit()
    return
