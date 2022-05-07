import sys

import psutil
from PySide6.QtCore import QCoreApplication, Qt, QThread, QUrl, QPoint
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
)
from lcu_ui import Ui_MainWindow
from utils import *


class LCUFixTool(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        self.lol_path: str = None
        self.server_data: Server_Info = None
        self.app = QApplication(sys.argv)
        super(LCUFixTool, self).__init__(*args, **kwargs)

        self.setupUi(self)  # 初始化ui
        # 隐藏系统标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 窗口拖动功能实现
        self.m_last_pos: QPoint = None
        # 检查本地配置
        self.check_local()
        # 进度条置零
        self.progressBar.setValue(0)
        # 选择目录按钮事件绑定
        self.manual_operation.clicked.connect(self.select_path)
        # 功能列表点击事件绑定
        self.options_widget.itemChanged.connect(self.item_checked)
        # 重载客户端点击事件绑定
        self.restart.clicked.connect(self.reload_client)
        # 净化客户端点击事件绑定
        self.smtx.clicked.connect(self.clean_client)
        # 检查更新
        self.check_update()

    # 检查本地配置
    def check_local(self):
        import json

        cfg_file = Path("~/Documents/LCUFixTool/config.json")
        cfg_file = cfg_file.expanduser()
        with cfg_file.open("r") as f:
            config = json.load(f)
        self.lol_path = config["lol"]
        self.path_show.setText(self.lol_path)
        self.path_show.setEnabled(True)

    # 重载功能列表
    def reload(self):
        if self.lol_path is None:
            return
        self.options_widget.clear()
        for wad_class_name in self.server_data.data:
            _item = QListWidgetItem(wad_class_name)
            # 取self.data[wad_class_name]的所有元素，并且把它们的安装状态设置取且运算
            _item.setCheckState(
                Qt.Checked
                if all(
                    [
                        get_lol_wad_status(self.lol_path, wad_name)
                        for wad_name in self.server_data.data[wad_class_name]
                    ]
                )
                else Qt.Unchecked
            )
            self.options_widget.addItem(_item)

    # 功能功能列表点击事件
    def item_checked(self, item: QListWidgetItem):
        if item.checkState() == Qt.Unchecked:
            for item in self.server_data.data[item.text()]:
                set_lol_wad_status(self.lol_path, item, False)
        else:
            for item in self.server_data.data[item.text()]:
                wad_path = Path(self.lol_path, item.path).parent / item.name
                if not wad_path.exists():
                    uri = self.server_data.host + item.name
                    # 用QThread开启线程下载
                    class DownloadThread(QThread):
                        def __init__(
                            self,
                            uri,
                            wad_path,
                            progressBar: QProgressBar,
                            *args,
                            **kwargs,
                        ):
                            super(DownloadThread, self).__init__(*args, **kwargs)
                            self.uri = uri
                            self.wad_path = wad_path
                            self.progressBar = progressBar

                        def run(self):
                            download_wad(uri, wad_path, self.progressBar)

                    thread = DownloadThread(uri, wad_path, self.progressBar)
                    thread.start()
                    # 等待线程结束
                    thread.wait()
                    # 进度条归零
                    self.progressBar.setValue(0)
                set_lol_wad_status(self.lol_path, item, True)
        self.reload()

    # 检查更新
    def check_update(self):
        from json import loads

        self.server_data = None
        request = QNetworkRequest(
            QUrl(
                "https://ghproxy.com/https://raw.githubusercontent.com/ASTWY/LCUFixTool/dev/data.json"
            )
        )
        response = QNetworkAccessManager(QCoreApplication.instance()).get(request)

        # 回调函数
        def call_back():
            # 把服务器返回的数据转换成字符串
            data = response.readAll().data().decode("utf-8")
            if data == "":
                raise "获取云端数据失败"
            self.server_data = Server_Info(**loads(data))
            self.reload()
            if self.server_data.msgContorl:
                _msg = self.server_data.msg
                self.message.setText(_msg)
                self.message.setOpenExternalLinks(True)
            else:
                self.message.setHidden(True)
            self.label_15.setText(
                f'当前支持版本：<font color="#FF0000">{self.server_data.ver}</font>'
            )

        response.finished.connect(call_back)

    # 开启一个目录选择窗口并获取选择的目录路径作为全局lol_path
    def select_path(self):
        tmp = QFileDialog.getExistingDirectory(
            self,
            QCoreApplication.translate("MainWindow", "请选择英雄联盟安装目录", None),
        )
        if check_lol_path(tmp):
            import json

            self.lol_path = check_lol_path(tmp)
            # 保存LOL目录
            cfg_file = Path("~/Documents/LCUFixTool/config.json")
            cfg_file = cfg_file.expanduser()
            if not cfg_file.parent.exists():
                cfg_file.parent.mkdir(parents=True)
            with cfg_file.open("r+") as f:
                config = json.load(f)
                config["lol"] = self.lol_path
                f.seek(0)
                f.truncate()
                json.dump(config, f)
            # 功能列表更新
            self.reload()
            self.path_show.setText(self.lol_path)
            self.about_close.setEnabled(True)
        else:
            # 错误弹窗提示
            QMessageBox.warning(
                self,
                QCoreApplication.translate("MainWindow", "错误", None),
                QCoreApplication.translate("MainWindow", "请选择正确的英雄联盟安装目录", None),
            )
            self.about_close.setEnabled(False)

    # 重载客户端
    def reload_client(self):
        # 判断是否以管理员权限运行
        if not is_admin():
            # 错误弹窗提示
            QMessageBox.warning(
                self,
                QCoreApplication.translate("MainWindow", "错误", None),
                QCoreApplication.translate("MainWindow", "请以管理员权限运行", None),
            )
            return
        # 取得进程列表
        for pid in psutil.pids():
            # 取得进程对象
            p = psutil.Process(pid)
            # 判断进程名是否为LeagueClientUxRender.exe
            if p.name() == "LeagueClientUxRender.exe":
                # 杀死进程
                p.kill()

    # 净化客户端
    def clean_client(self):
        import json

        # 提示确认
        if (
            QMessageBox.question(
                self,
                QCoreApplication.translate("MainWindow", "确认", None),
                QCoreApplication.translate(
                    "MainWindow", "该功能只能通过登录程序或Wegame修复才能恢复，你确认要继续执行吗？", None
                ),
            )
            == QMessageBox.Yes
        ):
            config_path = (
                Path(self.lol_path) / "LeagueClient/Plugins/plugin-manifest.json"
            )
            if config_path.exists():
                with config_path.open("r+", encoding="utf-8") as f:
                    data = json.load(f)
                    p = 0
                    i = 0
                    while True:
                        if i == len(data["plugins"]):
                            break
                        item = data["plugins"][i]
                        if item["name"] in ["rcp-fe-rpcs", "rcp-fe-gdp-live"]:
                            data["plugins"].remove(item)
                            i -= 1
                            p += 1
                            if p == 2:
                                break
                        i += 1
                    f.seek(0)
                    f.truncate()
                    f.write(
                        json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)
                    )
                # 提示
                QMessageBox.information(
                    self,
                    QCoreApplication.translate("MainWindow", "提示", None),
                    QCoreApplication.translate("MainWindow", "客户端已净化完成，请重新登录", None),
                )

    # 重写mousePressEvent、mouseMoveEvent函数,以实现窗口拖动
    def mousePressEvent(self, event):
        self.m_last_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        p = event.globalPosition().toPoint()
        self.move(
            self.x() + (p.x() - self.m_last_pos.x()),
            self.y() + (p.y() - self.m_last_pos.y()),
        )
        self.m_last_pos = event.globalPosition().toPoint()


if __name__ == "__main__":  # 程序的入口
    print("<a href=\"https://www.baidu.com\">百度一下</a>")
    try:
        app = LCUFixTool()
        app.show()
        sys.exit(app.app.exec())  # 进入事件循环
    except Exception as e:
        print(e)
