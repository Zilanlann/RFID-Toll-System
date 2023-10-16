import sys

from PyQt6.QtCore import QThread, QMutex, QWaitCondition, QMutexLocker, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox, QLineEdit, \
    QHBoxLayout, QProgressBar

from db_connections import *
from link_serial import *


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.thread_running = False  # 标记线程是否正在运行
        self.setup_ui()
        self.setup_thread()

    def setup_ui(self):
        # 创建按钮
        self.button_add_car = QPushButton("添加车辆")
        self.button_goto_normal = QPushButton("进入运营模式")
        self.button_pause_normal = QPushButton("暂停运营模式")
        self.button_resume_normal = QPushButton("继续运营模式")
        self.button_leave_normal = QPushButton("退出运营模式")

        # 创建QLabel
        self.carLabel = QLabel('请输入车牌号')
        self.carLineEdit = QLineEdit("")

        # 将按钮连接到相关函数
        self.button_add_car.clicked.connect(self.add_car)
        self.button_goto_normal.clicked.connect(self.start_thread)
        self.button_pause_normal.clicked.connect(self.paused_thread)
        self.button_resume_normal.clicked.connect(self.resume_thread)
        self.button_leave_normal.clicked.connect(self.stop_thread)
        self.progressBar = QProgressBar(self)
        layout_car = QHBoxLayout()
        layout_car.addWidget(self.carLabel)
        layout_car.addWidget(self.carLineEdit)
        # 创建布局并添加小部件
        layout = QVBoxLayout()
        layout.addLayout(layout_car)
        layout.addWidget(self.button_add_car)
        layout.addWidget(self.button_goto_normal)
        layout.addWidget(self.button_pause_normal)
        layout.addWidget(self.button_resume_normal)
        # layout.addWidget(self.button_leave_normal)

        self.setLayout(layout)

        self.setWindowTitle("RFID智能停车场管理系统")
        self.setGeometry(100, 100, 300, 200)
        self.center()

    def center(self):
        """将主程序窗口居中"""
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def add_car(self):
        """将文本框里输入的值车牌号与检测到的IC卡号一起存入数据库"""
        QMessageBox.information(self, "提示", "请将IC卡放置到检测区域，两个小灯全闪烁即为添加成功！")
        rfid_tag = get_card_id(ser)
        # sleep(2)
        # rfid_tag = "FFFFFF"
        license_plate = self.carLineEdit.text()
        add_new_car(license_plate, rfid_tag)
        QMessageBox.information(self, "提示", "车辆添加成功！")
        send(ser, "A1#")
        sleep(0.5)
        send(ser, "A0#")

    def setup_thread(self):
        self.thread = MyThread()
        self.thread.card_status.connect(self.act)
        self.thread_running = True

    def act(self, status):
        if status == -1:
            QMessageBox.information(self, "提示", f"进入停车场，开始计费{status}")
        elif status == -2:
            QMessageBox.information(self, "提示", "该车未注册！！！")
        else:
            QMessageBox.information(self, "提示", f"离开停车场，收费{status}元")

    def start_thread(self):
        QMessageBox.information(self, "提示", "已进入运营模式，将持续检测IC卡")
        if self.thread_running:
            self.thread.start()
        if not self.thread_running:
            self.setup_thread()
            self.thread.start()

    def paused_thread(self):
        if not self.thread_running:
            return
        if not self.thread.isRunning():
            self.thread.start()
        else:
            self.thread.pause_thread()

    def resume_thread(self):
        if not self.thread_running:
            return
        self.thread.resume_thread()

    def stop_thread(self):
        QMessageBox.information(self, "提示", "已退出运营模式")
        self.thread.quit()  # 终止线程的事件循环
        self.thread_running = False  # 标记线程停止


class MyThread(QThread):
    card_status = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.is_paused = bool(0)  # 标记线程是否暂停
        self.mutex = QMutex()  # 互斥锁，用于线程同步
        self.cond = QWaitCondition()  # 等待条件，用于线程暂停和恢复

    def pause_thread(self):
        with QMutexLocker(self.mutex):
            self.is_paused = True  # 设置线程为暂停状态

    def resume_thread(self):
        if self.is_paused:
            with QMutexLocker(self.mutex):
                self.is_paused = False  # 设置线程为非暂停状态
                self.cond.wakeOne()  # 唤醒一个等待的线程

    def run(self):
        while True:
            with QMutexLocker(self.mutex):
                while self.is_paused:
                    self.cond.wait(self.mutex)  # 当线程暂停时，等待条件满足
                # 检测IC卡
                rfid_tag = get_card_id(ser)
                # rfid_tag = "FFFFF"
                tmp = determine_entry_or_exit(rfid_tag)
                if tmp == -2:
                    self.card_status.emit(-2)
                elif tmp == -1:
                    self.card_status.emit(-1)
                else:
                    self.card_status.emit(tmp)
                self.sleep(1)


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    init_table()
    ser = init_serial()
    # print(determine_entry_or_exit(get_card_id(ser)))
    # print(get_card_id(ser))
    # send(ser, "A1#")
    # sleep(5)
    # send(ser, "A0#")
    main()
    # delete_all()
