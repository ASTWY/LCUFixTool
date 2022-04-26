import sys

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractScrollArea,
    QApplication,
    QFrame,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QWidget,
)

from utils import *


# 功能列表
class ListWidget(QListWidget):
    def __init__(self) -> None:
        super().__init__()
        self.reload()

    def reload(self):
        self.clear()
        server_info = get_server_info(
            "https://gitee.com/ASTWY/lcufix-tool/raw/master/version.json"
        )
        for item in server_info.data:
            item = QListWidgetItem(item.class_)
            item.setCheckState(Qt.Checked)
            self.addItem(item)


class LCUFixTool(object):
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.setup()
        sys.exit(self.app.exec())

    def setup(self):
        self.window = QMainWindow()
        self.window.setFont(QFont("Microsoft YaHei", 10))
        self.window.setWindowTitle("LCUFixTool")
        self.window.resize(800, 600)
        self.window.setMinimumSize(QSize(740, 550))
        self.window.setMaximumSize(QSize(740, 550))
        # 移除最大及最小化按钮
        self.window.setWindowFlags(Qt.WindowCloseButtonHint)

        self.centralwidget = QWidget(self.window)
        self.centralwidget.setObjectName("centralwidget")
        self.options_widget = QListWidget(self.centralwidget)
        self.options_widget.setObjectName("options_widget")
        self.options_widget.setGeometry(QRect(20, 90, 311, 311))
        font = QFont()
        font.setPointSize(12)
        self.options_widget.setFont(font)
        self.options_widget.setStyleSheet(
            "background-color:rgba(255, 255, 255, 0);"
            "border:1px solid rgb(255, 255, 255, 0);"
            ";"
            "color: rgb(0, 0, 0);"
        )
        self.options_widget.setFrameShadow(QFrame.Plain)
        self.options_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # 添加功能列表到主窗口
        self.listWidget = ListWidget()
        self.window.setCentralWidget(self.options_widget)
        # 显示窗口
        self.window.show()


if __name__ == "__main__":
    try:
        LCUFixTool()
    except Exception as e:
        print(e)
