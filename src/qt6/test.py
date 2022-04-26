import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from lcu_ui import Ui_MainWindow


class myWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):

        super(myWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)  # 初始化ui

        # 在这里，可以做一些UI的操作了，或者是点击事件或者是别的

        # 也可以另外写方法，可以改变lable的内容


if __name__ == "__main__":  # 程序的入口

    app = QApplication(sys.argv)

    win = myWindow()

    win.show()

    sys.exit(app.exec())
