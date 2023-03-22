import json
import sys
import urllib
from pathlib import Path

import psutil
from lcu_ui import Ui_MainWindow
from model import Server_Info
from PySide6.QtCore import (
    QCoreApplication,
    QPoint,
    QRunnable,
    Qt,
    QThread,
    QThreadPool,
    Signal,
)
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QProgressBar,
)
from utils import (
    check_lol_path,
    download_wad,
    get_lol_wad_status,
    get_user_data_path,
    is_admin,
    set_lol_wad_status,
)


class DownloadThread(QThread):
    """下载线程类"""

    progressChanged = Signal(float)  # 下载进度变化信号

    def __init__(self, url, filePath, parent=None):
        super().__init__(parent)
        self.url = url
        self.filePath = filePath

    def run(self):
        """下载文件"""
        with urllib.request.urlopen(self.url) as response:
            total_size = int(response.info()["Content-Length"])
            downloaded_size = 0
            with open("downloaded_file", "wb") as f:
                while True:
                    data = response.read(8192)
                    if not data:
                        break
                    downloaded_size += len(data)
                    f.write(data)
                    progress = downloaded_size / total_size * 100
                    self.progressChanged.emit(progress)


class DownloadQueue:
    """下载队列类"""

    def __init__(self):
        self.queue = []

    def add_task(self, url):
        """添加下载任务"""
        self.queue.append(url)

    def get_task(self):
        """获取一个下载任务"""
        if self.queue:
            return self.queue.pop(0)
        else:
            return None

    def task_count(self):
        """获取剩余任务数量"""
        return len(self.queue)


class LCUFixTool(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        self.lol_path: str = None
        self.server_data: Server_Info = None
        self.app = QApplication(sys.argv)
        super(LCUFixTool, self).__init__(*args, **kwargs)

        self.setupUi(self)  # 初始化ui
        # 隐藏系统标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 隐藏进度条标题
        self.current_operation.setVisible(False)
        # 超链接设置
        self.label_12.setOpenExternalLinks(True)
        self.label_13.setOpenExternalLinks(True)
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

        cfg_file = get_user_data_path() / "config.json"
        if cfg_file.exists():
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
                thread: DownloadThread = None
                if not wad_path.exists():
                    uri = self.server_data.host + item.name

                else:
                    set_lol_wad_status(self.lol_path, item, True)
        self.reload()

    # 检查更新
    def check_update(self):
        self.server_data = None
        client = Client(timeout=5, verify=False)
        # 获取服务器数据
        response = client.get(
            "https://raw.githubusercontent.com/ASTWY/LCUFixTool/dev/data.json"
        )
        if response.status_code == 200:
            self.server_data = Server_Info(**response.json())
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
        else:
            # 弹出错误提示
            QMessageBox.critical(
                self,
                "错误",
                "无法连接到服务器，请检查网络连接！",
                QMessageBox.Ok,
            )
            # 退出程序
            sys.exit(0)

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
            cfg_file = get_user_data_path() / "config.json"
            if not cfg_file.exists():
                if not cfg_file.parent.exists():
                    cfg_file.parent.mkdir(parents=True)
                # 以写入模式打开文件
                with cfg_file.open("w", encoding="utf-8") as f:
                    config = {"lol": self.lol_path}
                    json.dump(config, f)
            else:
                # 以读写模式打开文件
                with cfg_file.open("r+", encoding="utf-8") as f:
                    config = json.load(f)
                    config["lol"] = self.lol_path
                    f.seek(0)  # 将文件指针移到文件开头
                    f.truncate()  # 清空文件
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
    try:
        app = LCUFixTool()
        app.show()
        sys.exit(app.app.exec())  # 进入事件循环
    except Exception as e:
        # 弹出错误提示
        QMessageBox.critical(
            app,
            "错误",
            f"程序出现错误，请联系开发者！\n错误信息：{e}",
            QMessageBox.Ok,
        )
