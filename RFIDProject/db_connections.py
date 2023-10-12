import pymysql

# 连接到MySQL数据库
cnx = pymysql.connect(
    host="localhost",
    db="mysql",
    user="root",
    password="kiwMmya7xtS%DE"
)
cursor = cnx.cursor()

# 创建表
create_table_query = """
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT,
    department VARCHAR(255)
)
"""
cursor.execute(create_table_query)

# 插入数据
insert_data_query = """
INSERT INTO employees (name, age, department)
VALUES ('张三', 30, '技术部'),
       ('李四', 28, '市场部'),
       ('王五', 35, '人事部')
"""
cursor.execute(insert_data_query)
cnx.commit()

# 查询数据
select_data_query = "SELECT * FROM employees"
cursor.execute(select_data_query)

# 打印查询结果
for row in cursor:
    print(row)

# 删除数据
delete_data_query = "DELETE FROM employees WHERE id=1"
cursor.execute(delete_data_query)
cnx.commit()

# 关闭游标和连接
cursor.close()
cnx.close()
