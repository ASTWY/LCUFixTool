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
            "https://ghproxy.fsofso.com/https://github.com/ASTWY/LCUFixTool/blob/dev/version.json"
        )
        for item in server_info.data:
            item = QListWidgetItem(item.class_)
            item.setCheckState(Qt.Checked)
            self.addItem(item)


class LCUFixTool(object):


if __name__ == "__main__":
    try:
        LCUFixTool()
    except Exception as e:
        print(e)
