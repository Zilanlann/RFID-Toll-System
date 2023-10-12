from db_connections import *
from link_serial import *

if __name__ == '__main__':
    serial = serial.Serial('COM10', 9600, timeout=0.5)
    if serial.isOpen():
        print("open success")
    else:
        print("open failed")

    # 这里如果不加上一个while True，程序执行一次就自动跳出了
    while True:
        a = input("输入要发送的数据：")
        #
        if a == "exit":
            break
        send(a)
        while True:
            sleep(0.5)  # 起到一个延时的效果
            data = recv(serial)
            if data.decode('ascii') != '':
                print("receive: ", data.decode('ascii'))
                # break
    init_table()
    # 调用函数来检查是否存在特定的 car 值
    add_new_car("苏J99999", "FF1FF1")
    car_exists = check_car_exists("苏J99999")

    if car_exists:
        print("Car exists in the database.")
    else:
        print("Car does not exist in the database.")

    cursor.close()
    db.close()
