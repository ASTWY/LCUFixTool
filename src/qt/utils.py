from ctypes import windll
from hashlib import md5
from json import dump, load
from pathlib import Path
from typing import Union

from model import WAD_Info
from PySide6.QtWidgets import QProgressBar
from win32api import HIWORD, LOWORD, GetFileVersionInfo


# 计算文件MD5
def get_md5(file_path: str) -> str:
    d5 = md5()
    file_path: Path = Path(file_path)
    with file_path.open("rb") as f:
        while True:
            data = f.read(2024)
            if not data:
                break
            d5.update(data)  # update添加时会进行计算
    return d5.hexdigest().upper()


def is_admin() -> bool:
    """
    WindowsAPI判断是否以管理员身份运行
    """
    try:
        return windll.shell32.IsUserAnAdmin()
    except Exception:
        return False
    # open("//./PHYSICALDRIVE0", "r")
    # return True


# 检查LOL路径是否正确
def check_lol_path(lol_path: str) -> Union[bool, str]:
    _path = Path(lol_path)
    if _path.joinpath("LeagueClient/LeagueClient.exe").exists():
        return lol_path
    elif _path.joinpath("League of Legends.exe").exists():
        return _path.parent.__str__()
    return False


# 获取LOL的版本号,返回第一个点前后的两位数字
def get_lol_version(lol_path: str) -> Union[str, bool]:
    """
    获取LOL的版本号
    :param lol_path: LOL的安装路径
    :return: LOL的版本号
    """
    if not Path(lol_path).exists():
        return False
    try:
        version_info = GetFileVersionInfo(lol_path, "\\")
        version = version_info["FileVersionMS"]
        return f"{HIWORD(version)}.{LOWORD(version)}"
    except Exception:
        return False


# 获取LOL wad 模块安装状态
def get_lol_wad_status(lol_path: str, wad_info: WAD_Info) -> bool:
    cfg_path = Path(lol_path) / wad_info.path
    wad_path = Path(lol_path, wad_info.path).parent / wad_info.name
    if wad_path.exists():
        # 校验wad文件md5
        if get_md5(wad_path) != wad_info.md5:
            try:
                wad_path.unlink()
                # 设置wad模块安装状态为False
                set_lol_wad_status(lol_path, wad_info, False)
            except Exception:
                return False
    else:
        # 设置wad模块安装状态为False
        set_lol_wad_status(lol_path, wad_info, False)
    if cfg_path.exists():
        with cfg_path.open("r", encoding="utf-8") as f:
            cfg_data = load(f)
            if wad_info.type == "add":
                if wad_info.name in cfg_data["riotMeta"]["globalAssetBundles"]:
                    return True
            elif wad_info.type == "cover":
                value = eval(f"cfg_data{wad_info.orgin_key}")
                if wad_info.name == value:
                    return True
    return False


# 设置LOL wad 模块安装状态
def set_lol_wad_status(lol_path: str, wad_info: WAD_Info, status: bool) -> bool:
    cfg_json_path = Path(lol_path) / wad_info.path
    if cfg_json_path.exists():
        with cfg_json_path.open("r+", encoding="utf-8") as f:
            cfg_data = load(f)
            if wad_info.type == "add":
                if status:
                    if wad_info.name not in cfg_data["riotMeta"]["globalAssetBundles"]:
                        cfg_data["riotMeta"]["globalAssetBundles"].append(wad_info.name)
                else:
                    # 删除列表中的元素
                    if wad_info.name in cfg_data["riotMeta"]["globalAssetBundles"]:
                        cfg_data["riotMeta"]["globalAssetBundles"].remove(wad_info.name)
            elif wad_info.type == "cover":
                if status:
                    exec(f"cfg_data{wad_info.orgin_key} = wad_info.name")
                else:
                    exec(f"cfg_data{wad_info.orgin_key} = wad_info.orgin_value")
            # 用cfg_data覆盖文件
            f.seek(0)
            f.truncate()
            dump(cfg_data, f, ensure_ascii=False, indent=4)


# 下载wad文件，并将进度信息显示在QT进度条上
def download_wad(url: str, file_path: str, progress_bar: QProgressBar) -> bool:
    """
    下载wad文件，并将进度信息显示在QT进度条上
    :param url: wad文件的url
    :param file_path: wad文件的路径
    :param progress_bar: QT进度条
    :return: True or False
    """
    if not url or not file_path:
        return False
    file_path = Path(file_path)
    try:
        with stream("GET", url) as response:
            if response.status_code == 200:
                # 获取文件大小
                file_size = int(response.headers["Content-Length"])
                # 设置进度条的最大值
                progress_bar.setMaximum(file_size)
                # 设置进度条的当前值
                progress_bar.setValue(0)
                with file_path.open("wb") as f:
                    for chunk in response.iter_bytes(1024):
                        if chunk:
                            f.write(chunk)
                            # 设置进度条的当前值
                            progress_bar.setValue(f.tell())
            return True
    except Exception:
        try:
            file_path.unlink()
        except Exception:
            pass
        return False


# 获取用户数据目录
def get_user_data_path(path: str = None) -> Path:
    """
    获取用户数据目录
    :return: 用户数据目录
    """
    data_path = Path("~/Documents/LCUFixTool").expanduser()
    if path:
        data_path = data_path.joinpath(path)
    if not data_path.exists():
        try:
            data_path.parent.mkdir(parents=True)
        except Exception:
            pass
    return data_path
