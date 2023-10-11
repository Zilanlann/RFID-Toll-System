import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.statusBar().showMessage('Ready')
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.clicked.connect(self.button_clicked)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Statusbar')

        self.show()

    def button_clicked(self):
        self.statusBar().showMessage('Really')

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
