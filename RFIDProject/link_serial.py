from time import sleep

import serial


def init_serial():
    ser = serial.Serial('COM10', 9600, timeout=0.5)
    if ser.isOpen():
        print("串口打开成功")
    else:
        print("串口打开失败")
    return ser


def recv(ser):
    while True:
        data = ser.read_all()
        if data == '':
            continue
        else:
            break
        sleep(0.02)
    return data


def send(ser, send_data):
    if ser.isOpen():
        ser.write(send_data.encode('utf-8'))  # 编码
    else:
        print("发送失败！")


def get_card_id(ser):
    send(ser, "IC#")
    while True:
        sleep(0.5)  # 起到一个延时的效果
        data = recv(ser)
        if data.decode('ascii') != '':
            return data.decode('ascii')
