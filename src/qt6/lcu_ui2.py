# -*- coding: utf-8 -*-

from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QRect,
    QSize,
    Qt,
)
from PySide6.QtGui import (
    QFont,
    QIcon,
    QPixmap,
)
from PySide6.QtWidgets import (
    QAbstractScrollArea,
    QFrame,
    QLabel,
    QLineEdit,
    QListWidget,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QWidget,
)
import lcu_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(740, 550)
        MainWindow.setMinimumSize(QSize(740, 550))
        MainWindow.setMaximumSize(QSize(740, 550))
        # 隐藏标题栏
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.smtx = QPushButton(self.centralwidget)
        self.smtx.setObjectName("smtx")
        self.smtx.setGeometry(QRect(20, 380, 311, 41))
        font = QFont()
        font.setFamilies(["\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(13)
        font.setBold(True)
        self.smtx.setFont(font)
        self.smtx.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "background-color:rgb(200, 74, 76);\n"
            "color:white;\n"
            "border-radius:5px;\n"
            "}\n"
            "QPushButton::hover{\n"
            "background-color:rgb(170, 74, 76);\n"
            "}\n"
            "\n"
            "QPushButton::pressed{\n"
            "background-color:rgb(165, 54, 76);\n"
            "}\n"
            ""
        )
        self.smtx.setFlat(True)
        self.options_widget = QListWidget(self.centralwidget)
        self.options_widget.setObjectName("options_widget")
        self.options_widget.setGeometry(QRect(20, 110, 311, 231))
        font1 = QFont()
        font1.setPointSize(12)
        self.options_widget.setFont(font1)
        self.options_widget.setStyleSheet(
            "background-color:rgba(255, 255, 255, 0);\n"
            "border:1px solid rgb(255, 255, 255, 0);\n"
            ";\n"
            "color: rgb(0, 0, 0);"
        )
        self.options_widget.setFrameShadow(QFrame.Plain)
        self.options_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setGeometry(QRect(400, 510, 311, 15))
        self.progressBar.setStyleSheet(
            "QProgressBar{\n"
            "border: none;\n"
            "color: white;\n"
            "text-align: center;\n"
            "background: rgb(68, 69, 73);\n"
            "}\n"
            "QProgressBar::chunk {\n"
            "border: none;\n"
            "background: rgb(0, 160, 230);\n"
            "}"
        )
        self.progressBar.setValue(12)
        self.progressBar.setTextVisible(False)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.label_3.setGeometry(QRect(0, 0, 741, 550))
        self.label_3.setStyleSheet(
            "background-image: url(:/img/riot-background.png);\n" ""
        )
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.label_4.setGeometry(QRect(370, 0, 370, 551))
        self.label_4.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0.584955, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 90));"
        )
        self.current_operation = QLabel(self.centralwidget)
        self.current_operation.setObjectName("current_operation")
        self.current_operation.setGeometry(QRect(400, 470, 261, 21))
        font2 = QFont()
        font2.setFamilies(["\u5fae\u8f6f\u96c5\u9ed1"])
        font2.setPointSize(15)
        font2.setBold(True)
        self.current_operation.setFont(font2)
        self.current_operation.setStyleSheet("color: rgb(255, 255, 255);")
        self.close_window = QPushButton(self.centralwidget)
        self.close_window.setObjectName("close_window")
        self.close_window.setGeometry(QRect(700, 0, 41, 25))
        self.close_window.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "background-color: rgb(255, 255, 255,0);\n"
            "border:1px solid rgb(255, 255, 255, 0);\n"
            "}\n"
            "QPushButton::hover{\n"
            "background-color: rgba(255, 0, 0, 90);\n"
            "}\n"
            "QPushButton::pressed{\n"
            "background-color: rgb(255, 0, 0,180);\n"
            "}\n"
            "\n"
            ""
        )
        icon = QIcon()
        icon.addFile(":/img/close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.close_window.setIcon(icon)
        self.minimize = QPushButton(self.centralwidget)
        self.minimize.setObjectName("minimize")
        self.minimize.setGeometry(QRect(660, 0, 41, 25))
        self.minimize.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "background-color: rgb(255, 255, 255,0);\n"
            "border:1px solid rgb(255, 255, 255, 0);\n"
            "}\n"
            "QPushButton::hover{\n"
            "background-color: rgb(255, 255, 255,100);\n"
            "}\n"
            "QPushButton::pressed{\n"
            "background-color: rgb(255, 255, 255,150);\n"
            "}\n"
            "\n"
            ""
        )
        icon1 = QIcon()
        icon1.addFile(":/img/icon_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimize.setIcon(icon1)
        self.program_title = QLabel(self.centralwidget)
        self.program_title.setObjectName("program_title")
        self.program_title.setGeometry(QRect(10, 0, 221, 21))
        font3 = QFont()
        font3.setFamilies(["\u5fae\u8f6f\u96c5\u9ed1"])
        font3.setPointSize(10)
        self.program_title.setFont(font3)
        self.program_title.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.label_5.setGeometry(QRect(0, 0, 370, 551))
        font4 = QFont()
        font4.setPointSize(8)
        self.label_5.setFont(font4)
        self.label_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(470, 160, 145, 151))
        self.label.setPixmap(QPixmap(":/img/lol_icon.png"))
        self.label.setScaledContents(True)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.label_6.setGeometry(QRect(380, 310, 321, 41))
        font5 = QFont()
        font5.setFamilies(["\u5fae\u8f6f\u96c5\u9ed1"])
        font5.setPointSize(20)
        font5.setBold(True)
        self.label_6.setFont(font5)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_6.setAlignment(Qt.AlignCenter)
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.label_7.setGeometry(QRect(380, 350, 321, 20))
        self.label_7.setFont(font3)
        self.label_7.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_7.setAlignment(Qt.AlignCenter)
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.label_8.setGeometry(QRect(20, 50, 211, 31))
        font6 = QFont()
        font6.setFamilies(["\u5fae\u8f6f\u96c5\u9ed1"])
        font6.setPointSize(18)
        font6.setBold(True)
        self.label_8.setFont(font6)
        self.about_frame = QFrame(self.centralwidget)
        self.about_frame.setObjectName("about_frame")
        self.about_frame.setGeometry(QRect(-1, -1, 741, 551))
        self.about_frame.setStyleSheet("background-color: rgba(0, 0, 0, 245);")
        self.about_frame.setFrameShape(QFrame.StyledPanel)
        self.about_frame.setFrameShadow(QFrame.Raised)
        self.label_10 = QLabel(self.about_frame)
        self.label_10.setObjectName("label_10")
        self.label_10.setGeometry(QRect(70, 90, 111, 31))
        self.label_10.setFont(font5)
        self.label_10.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0);\n" "color: rgb(255, 255, 255);"
        )
        self.path = QFrame(self.about_frame)
        self.path.setObjectName("path")
        self.path.setGeometry(QRect(70, 130, 601, 51))
        self.path.setStyleSheet(
            "background-color: rgb(55, 55, 55);\n" "border-radius:8px;"
        )
        self.path.setFrameShape(QFrame.StyledPanel)
        self.path.setFrameShadow(QFrame.Raised)
        self.path_show = QLineEdit(self.path)
        self.path_show.setObjectName("path_show")
        self.path_show.setGeometry(QRect(30, 10, 451, 31))
        font7 = QFont()
        font7.setFamilies(["\u5fae\u8f6f\u96c5\u9ed1"])
        self.path_show.setFont(font7)
        self.path_show.setStyleSheet(
            "background-color: rgb(176, 176, 176,150);\n"
            "border:1px solid rgb(255, 255, 255, 0);\n"
            "border-radius:5px;"
        )
        self.path_show.setReadOnly(True)
        self.manual_operation = QPushButton(self.path)
        self.manual_operation.setObjectName("manual_operation")
        self.manual_operation.setGeometry(QRect(490, 10, 81, 31))
        font8 = QFont()
        font8.setFamilies(["\u5fae\u8f6f\u96c5\u9ed1"])
        font8.setBold(False)
        self.manual_operation.setFont(font8)
        self.manual_operation.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "background-color: rgb(90, 148, 255);\n"
            "color:white;\n"
            "border-radius:5px;\n"
            "}\n"
            "QPushButton::hover{\n"
            "background-color: rgb(80, 133, 226);\n"
            "}\n"
            "\n"
            "QPushButton::pressed{\n"
            "background-color:rgb(65, 113, 200);\n"
            "}\n"
            "\n"
            ""
        )
        self.about_close = QPushButton(self.about_frame)
        self.about_close.setObjectName("about_close")
        self.about_close.setGeometry(QRect(340, 440, 60, 60))
        self.about_close.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "background-color: rgb(114,115,117);\n"
            "border-radius:25px;\n"
            "color:white;\n"
            "}\n"
            "QPushButton::hover{\n"
            "background-color: rgb(158,159,160);\n"
            "}\n"
            "\n"
            "QPushButton::pressed{\n"
            "background-color:rgb(91,92,95);\n"
            "}\n"
            ""
        )
        self.about_close.setIcon(icon)
        self.about_close.setIconSize(QSize(30, 30))
        self.label_11 = QLabel(self.about_frame)
        self.label_11.setObjectName("label_11")
        self.label_11.setGeometry(QRect(70, 220, 111, 31))
        self.label_11.setFont(font5)
        self.label_11.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0);\n" "color: rgb(255, 255, 255);"
        )
        self.about = QFrame(self.about_frame)
        self.about.setObjectName("about")
        self.about.setGeometry(QRect(70, 260, 601, 121))
        self.about.setStyleSheet(
            "background-color: rgb(55, 55, 55);\n" "border-radius:8px;"
        )
        self.about.setFrameShape(QFrame.StyledPanel)
        self.about.setFrameShadow(QFrame.Raised)
        self.plainTextEdit_2 = QPlainTextEdit(self.about)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.plainTextEdit_2.setGeometry(QRect(20, 20, 551, 71))
        font9 = QFont()
        font9.setFamilies(["\u5fae\u8f6f\u96c5\u9ed1"])
        font9.setPointSize(12)
        self.plainTextEdit_2.setFont(font9)
        self.plainTextEdit_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.plainTextEdit_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.plainTextEdit_2.setReadOnly(True)
        self.restart = QPushButton(self.centralwidget)
        self.restart.setObjectName("restart")
        self.restart.setGeometry(QRect(20, 470, 311, 41))
        self.restart.setFont(font)
        self.restart.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "background-color: rgb(114,115,117);\n"
            "color:white;\n"
            "border-radius:5px;\n"
            "}\n"
            "QPushButton::hover{\n"
            "background-color: rgb(158,159,160);\n"
            "}\n"
            "\n"
            "QPushButton::pressed{\n"
            "background-color:rgb(91,92,95);\n"
            "}\n"
            ""
        )
        self.restart.setFlat(True)
        self.settings = QPushButton(self.centralwidget)
        self.settings.setObjectName("settings")
        self.settings.setGeometry(QRect(680, 470, 30, 30))
        self.settings.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "background-color: rgb(114,115,117);\n"
            "color:white;\n"
            "border-radius:5px;\n"
            "}\n"
            "QPushButton::hover{\n"
            "background-color: rgb(158,159,160);\n"
            "}\n"
            "\n"
            "QPushButton::pressed{\n"
            "background-color:rgb(91,92,95);\n"
            "}\n"
            ""
        )
        icon2 = QIcon()
        icon2.addFile(":/img/sq-setting.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settings.setIcon(icon2)
        self.notification_btn = QPushButton(self.centralwidget)
        self.notification_btn.setObjectName("notification_btn")
        self.notification_btn.setGeometry(QRect(310, 50, 21, 21))
        self.notification_btn.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "background-color: rgba(255, 255, 255, 0);\n"
            "border-image: url(:/img/notification.png);\n"
            "}\n"
            "QPushButton::hover{\n"
            "border-image: url(:/img/notification_hover.png);\n"
            "}\n"
            "QPushButton::pressed{\n"
            "border-image: url(:/img/notification_pressed.png);\n"
            "}\n"
            ""
        )
        self.notification_btn.setFlat(True)
        self.notification_frame = QFrame(self.centralwidget)
        self.notification_frame.setObjectName("notification_frame")
        self.notification_frame.setGeometry(QRect(370, 30, 361, 121))
        self.notification_frame.setFrameShape(QFrame.StyledPanel)
        self.notification_frame.setFrameShadow(QFrame.Raised)
        self.label_2 = QLabel(self.notification_frame)
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(QRect(20, 10, 331, 111))
        self.label_2.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n"
            "border-radius:5px;\n"
            "border-color: rgb(0, 0, 0);"
        )
        self.notification_close = QPushButton(self.notification_frame)
        self.notification_close.setObjectName("notification_close")
        self.notification_close.setGeometry(QRect(310, 10, 31, 25))
        self.notification_close.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "background-color: rgb(255, 255, 255,0);\n"
            "border:1px solid rgb(255, 255, 255, 0);\n"
            "}\n"
            "QPushButton::hover{\n"
            "background-color: rgba(255, 0, 0, 90);\n"
            "}\n"
            "QPushButton::pressed{\n"
            "background-color: rgb(255, 0, 0,180);\n"
            "}\n"
            "\n"
            ""
        )
        self.notification_close.setIcon(icon)
        self.label_9 = QLabel(self.notification_frame)
        self.label_9.setObjectName("label_9")
        self.label_9.setGeometry(QRect(33, 20, 61, 21))
        font10 = QFont()
        font10.setFamilies(["\u5fae\u8f6f\u96c5\u9ed1"])
        font10.setPointSize(12)
        font10.setBold(True)
        self.label_9.setFont(font10)
        self.plainTextEdit = QPlainTextEdit(self.notification_frame)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(30, 40, 311, 71))
        self.plainTextEdit.setFont(font3)
        self.plainTextEdit.setStyleSheet(
            "background-color: rgb(255, 255, 255,0);\n"
            "border:1px solid rgb(255, 255, 255, 0);\n"
            ""
        )
        self.plainTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.plainTextEdit.setReadOnly(True)
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName("label_12")
        self.label_12.setGeometry(QRect(390, 410, 321, 20))
        self.label_12.setFont(font3)
        self.label_12.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_12.setAlignment(Qt.AlignCenter)
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName("label_13")
        self.label_13.setGeometry(QRect(390, 390, 321, 20))
        self.label_13.setFont(font3)
        self.label_13.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_13.setAlignment(Qt.AlignCenter)
        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName("label_14")
        self.label_14.setGeometry(QRect(390, 430, 331, 20))
        self.label_14.setFont(font3)
        self.label_14.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_14.setAlignment(Qt.AlignCenter)
        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName("label_15")
        self.label_15.setGeometry(QRect(390, 370, 321, 20))
        self.label_15.setFont(font3)
        self.label_15.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_15.setAlignment(Qt.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.label_3.raise_()
        self.label_4.raise_()
        self.progressBar.raise_()
        self.current_operation.raise_()
        self.program_title.raise_()
        self.label_5.raise_()
        self.options_widget.raise_()
        self.smtx.raise_()
        self.label.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.restart.raise_()
        self.settings.raise_()
        self.notification_btn.raise_()
        self.notification_frame.raise_()
        self.label_12.raise_()
        self.label_13.raise_()
        self.label_14.raise_()
        self.close_window.raise_()
        self.minimize.raise_()
        self.label_15.raise_()
        self.about_frame.raise_()

        self.retranslateUi(MainWindow)
        self.about_close.clicked.connect(self.about_frame.hide)
        self.close_window.clicked.connect(MainWindow.close)
        self.minimize.clicked.connect(MainWindow.showMinimized)
        self.settings.clicked.connect(self.about_frame.show)
        self.notification_btn.clicked.connect(self.notification_frame.show)
        self.notification_close.clicked.connect(self.notification_frame.hide)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.smtx.setText(
            QCoreApplication.translate(
                "MainWindow", "\u51c0\u5316\u5ba2\u6237\u7aef", None
            )
        )
        self.label_3.setText("")
        self.label_4.setText("")
        self.current_operation.setText(
            QCoreApplication.translate("MainWindow", "下载进度", None)
        )
        self.program_title.setText(
            QCoreApplication.translate(
                "MainWindow", "LCU \u8fd8\u539f\uff08\u6807\u9898\uff09", None
            )
        )
        self.label_5.setText("")
        self.label.setText("")
        self.label_6.setText(
            QCoreApplication.translate(
                "MainWindow", "LCU\u66ff\u6362\u5de5\u5177", None
            )
        )
        self.label_7.setText(QCoreApplication.translate("MainWindow", "V2.0", None))
        self.label_8.setText(
            QCoreApplication.translate("MainWindow", "\u529f\u80fd", None)
        )
        self.label_10.setText(
            QCoreApplication.translate("MainWindow", "\u8def\u5f84", None)
        )
        self.path_show.setText("")
        self.path_show.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "\u6e38\u620f\u8def\u5f84", None)
        )
        self.manual_operation.setText(
            QCoreApplication.translate("MainWindow", "\u624b\u52a8\u9009\u62e9", None)
        )
        self.label_11.setText(
            QCoreApplication.translate("MainWindow", "\u5173\u4e8e", None)
        )
        self.plainTextEdit_2.setPlainText(
            QCoreApplication.translate(
                "MainWindow",
                "\u6240\u6709\u4fee\u6539\u65b9\u6cd5\u601d\u8def\u5747\u7531B\u7ad9 @ZYXeeker \u539f\u521b!\n"
                "\u672c\u5de5\u5177\u7531 @\u827e\u65af\u6258\u7ef4\u4e9a \u63d0\u4f9b\u6280\u672f\u652f\u6301!\n"
                "\u53ea\u4f5c\u4e2a\u4eba\u5b66\u4e60\u7814\u7a76\u7528\u9014\u516c\u5f00,\u4e0d\u627f\u62c5\u4efb\u4f55\u8d23\u4efb\u3002",
                None,
            )
        )
        self.restart.setText(
            QCoreApplication.translate(
                "MainWindow", "\u91cd\u8f7d\u5ba2\u6237\u7aef", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.settings.setToolTip(
            QCoreApplication.translate("MainWindow", "\u8bbe\u7f6e", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.settings.setText("")
        # if QT_CONFIG(tooltip)
        self.notification_btn.setToolTip(
            QCoreApplication.translate("MainWindow", "\u901a\u77e5", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.label_2.setText("")
        self.label_9.setText(
            QCoreApplication.translate("MainWindow", "\u63d0\u9192", None)
        )
        self.plainTextEdit.setPlainText(
            QCoreApplication.translate("MainWindow", "this is a notice", None)
        )
        self.label_12.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p>\u6240\u6709\u4fee\u6539\u65b9\u6cd5\u601d\u8def\u5747\u7531B\u7ad9 <a href="https://space.bilibili.com/186789482"><span style=" text-decoration: underline; color:#00ff7f;">@ZYXeeker</span></a> \u539f\u521b!</p></body></html>',
                None,
            )
        )
        self.label_13.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p>\u672c\u5de5\u5177\u7531 <a href="https://space.bilibili.com/86332521"><span style=" text-decoration: underline; color:#00ff7f;">@\u827e\u65af\u6258\u7ef4\u4e9a</span></a> \u63d0\u4f9b\u6280\u672f\u652f\u6301</p></body></html>',
                None,
            )
        )
        self.label_14.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u53ea\u4f5c\u4e2a\u4eba\u5b66\u4e60\u7814\u7a76\u7528\u9014\u516c\u5f00,\u4e0d\u627f\u62c5\u4efb\u4f55\u8d23\u4efb\uff01",
                None,
            )
        )
        self.label_15.setText(
            QCoreApplication.translate(
                "MainWindow",
                '\u5f53\u524d\u652f\u6301\u7248\u672c\uff1a<font color="#FF0000">12.7</font>',
                None,
            )
        )

    # retranslateUi
