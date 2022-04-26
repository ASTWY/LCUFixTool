from json import load
from pathlib import Path
from typing import Union

from httpx import get
from win32api import HIWORD, LOWORD, GetFileVersionInfo

from model import Server_Info, WAD_Info


# 获取云端数据
def get_server_info(server_url: str) -> Union[Server_Info, bool]:
    """
    获取云端数据
    :param server_url: 云端数据的url
    :return: 云端数据
    """
    if not server_url:
        return False
    try:
        resp = get(server_url)
        if resp.status_code == 200:
            return Server_Info(**resp.json())
    except:
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
    except:
        return False


# 获取LOL wad 模块安装状态
def get_lol_wad_status(lol_path: str, wad_info: WAD_Info) -> bool:
    from re import findall

    cfg_path = Path(lol_path) / wad_info.path
    if cfg_path.exists():
        with cfg_path.open("r", encoding="utf-8") as f:
            cfg_data = load(f)
            if wad_info.type == "add":
                if wad_info.name in cfg_data["riotMeta"]["globalAssetBundles"]:
                    return True
            elif wad_info.type == "cover":
                keys = findall(r"\['?(\w*)'?\]", wad_info.orgin_key)
                # 将keys中的元素作为key，取出cfg_data中对应的值的最后一个
                for i in range(len(keys)):
                    if i == 0:
                        value = cfg_data[keys[i]]
                    else:
                        if keys[i].isdigit():
                            value = value[int(keys[i])]
                        else:
                            value = value[keys[i]]
                if wad_info.name == value:
                    return True
    return False


# 设置LOL wad 模块安装状态
def set_lol_wad_status(lol_path: str, wad_info: WAD_Info, status: bool) -> bool:
    pass


if __name__ == "__main__":
    from httpx import get

    lol_path = "E:\Game\Riot Games\CN"
    resp = get("https://gitee.com/ASTWY/lcufix-tool/raw/master/version.json")
    server_info = Server_Info(**resp.json())
    for wad_info in server_info.data:
        print(f"{wad_info.note}:{get_lol_wad_status(lol_path, wad_info)}")
