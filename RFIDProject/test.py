import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 创建按钮
        self.button_show_message = QPushButton("Show Message")
        self.button_execute_function = QPushButton("Execute Function")

        # 创建QLabel
        self.label = QLabel("")

        # 将按钮连接到相关函数
        self.button_show_message.clicked.connect(self.show_message)
        self.button_execute_function.clicked.connect(self.execute_function)

        # 创建布局并添加小部件
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_show_message)
        layout.addWidget(self.button_execute_function)

        self.setLayout(layout)

        self.setWindowTitle("PyQt6 Example")
        self.setGeometry(100, 100, 300, 200)

    def show_message(self):
        QMessageBox.information(self, "Message", "Hello, PyQt6!")

    def execute_function(self):
        # 在这里执行您的自定义函数，返回文本
        output_info = "赵宇豪大傻逼"
        self.label.setText(output_info)

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
