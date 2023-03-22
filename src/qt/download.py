from urllib.request import urlopen
from ssl import create_default_context, CERT_NONE
from PySide6.QtCore import QThread, Signal

context = create_default_context()
context.check_hostname = False
context.verify_mode = CERT_NONE


class DownloadTask:
    """
    下载任务类
    """

    def __init__(self, url, savePath):
        self.url = url
        self.savePath = savePath


class DownloadQueue:
    """
    下载队列类
    """

    def __init__(self):
        self.queue = []

    def add_task(self, task: DownloadTask):
        """
        添加下载任务
        :param task: 下载任务
        """
        self.queue.append(task)

    def get_task(self):
        """
        获取一个下载任务
        :return: 下载任务
        """
        if self.queue:
            return self.queue.pop(0)
        else:
            return None

    def task_count(self):
        """
        获取剩余任务数量
        :return: 剩余任务数量
        """
        return len(self.queue)


class DownloadThread(QThread):
    """
    下载线程类
    """

    progressChanged = Signal(float)  # 下载进度变化信号
    finsihed = Signal()  # 下载完成信号

    def __init__(self, queue: DownloadQueue, parent=None):
        super().__init__(parent)
        self.queue = queue

    def run(self):
        """
        下载文件, 从队列中获取下载任务, 下载完成后发送下载完成信号
        """
        while True:
            task = self.queue.get_task()
            if task is None:
                break
            self.download(task)

    def download(self, task: DownloadTask):
        with urlopen(task.url, context=context) as response:
            total_size = int(response.info()["Content-Length"])
            downloaded_size = 0
            with open(task.savePath, "wb") as f:
                while True:
                    data = response.read(8192)
                    if not data:
                        break
                    downloaded_size += len(data)
                    f.write(data)
                    progress = downloaded_size / total_size * 100
                    self.progressChanged.emit(progress)
                self.finsihed.emit()  # 下载完成
