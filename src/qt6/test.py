import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from lcu_ui import Ui_MainWindow


class LCUFixTool(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        self.app = QApplication(sys.argv)
        super(LCUFixTool, self).__init__(*args, **kwargs)

        self.setupUi(self)  # 初始化ui

        # 在这里，可以做一些UI的操作了，或者是点击事件或者是别的

        # 也可以另外写方法，可以改变lable的内容


if __name__ == "__main__":  # 程序的入口
    try:
        app = LCUFixTool()
        app.show()
        sys.exit(app.app.exec())  # 进入事件循环
    except Exception as e:
        print(e)
    pass
