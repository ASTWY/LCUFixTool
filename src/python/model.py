from down import download_from_url
from requests import get


def GetConfig():
    res = get("https://gitee.com/ASTWY/lcufix-tool/raw/master/version.json")
    if res.status_code == 200:
        return res.json()


def GetMD5(file: str):
    import hashlib
    d5 = hashlib.md5()
    with open(file, 'rb') as f:
        while True:
            data = f.read(2024)
            if not data:
                break
            d5.update(data)  #update添加时会进行计算
    return d5.hexdigest().upper()


def getFileVersion(file_name):
    import win32api, os
    info = win32api.GetFileVersionInfo(file_name, os.sep)
    ms = info['FileVersionMS']
    # ls = info['FileVersionLS']
    version = '%d.%d' % (win32api.HIWORD(ms), win32api.LOWORD(ms))
    #                             win32api.HIWORD(ls), win32api.LOWORD(ls))
    return version


def GetLOLPath():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()

    t = filedialog.askdirectory(title="请选择英雄联盟安装目录")
    return t


def Set_or_Get_wad_state(lolpath: str, wadinfo, model="GET", downhost=""):
    import os, json
    #q = wadinfo['name']
    state = False  #当前模块状态
    _wad = os.path.join(lolpath,
                        os.path.join(os.path.dirname(wadinfo['path']),
                                     wadinfo['name']))  # wad文件路径
    # 如果wad文件不存在
    if not os.path.exists(_wad):
        if model == "SET":
            downUri = downhost + wadinfo['name']
            savePath = _wad
            download_from_url(downUri, savePath)
        elif model != "DEL":
            Set_or_Get_wad_state(lolpath, wadinfo, model="DEL")
    else:
        if model != "DEL":
            if (GetMD5(_wad) != wadinfo['md5']):
                Set_or_Get_wad_state(lolpath, wadinfo, model="DEL")
                os.remove(_wad)

    # 载入配置json文件
    data = json.load(
        open(os.path.join(lolpath, wadinfo['path']), "r",
             encoding="utf-8"))['riotMeta']

    if wadinfo['type'] == 'cover':
        if data['perLocaleAssetBundles']['zh_CN'][0] == wadinfo['name']:
            state = True
    else:
        _tmp = data['globalAssetBundles']
        if len(_tmp) > 1:
            if (wadinfo['name'] in _tmp) and (wadinfo['name'] != _tmp[0]):
                state = True
            pass

    #不同模式的不同处理
    if model == "GET":
        return state  # "[green]√\t[/green]" if state else "[red]×\t[/red]"
    elif model == "SET":
        if state:
            if wadinfo['type'] == 'cover':
                data['perLocaleAssetBundles']['zh_CN'][0] = wadinfo['orgin']
            else:
                if wadinfo['name'] in data['globalAssetBundles']:
                    data['globalAssetBundles'].remove(wadinfo['name'])
        else:
            if wadinfo['type'] == 'cover':
                data['perLocaleAssetBundles']['zh_CN'][0] = wadinfo['name']
            else:
                data['globalAssetBundles'].append(wadinfo['name'])
    elif model == "DEL":
        if wadinfo['type'] == 'cover':
            data['perLocaleAssetBundles']['zh_CN'][0] = wadinfo['orgin']
        else:
            if wadinfo['name'] in data['globalAssetBundles']:
                data['globalAssetBundles'].remove(wadinfo['name'])
    with open(os.path.join(lolpath, wadinfo['path']), "r+",
              encoding="utf-8") as f:
        _tmp1 = json.load(f)
        _tmp1['riotMeta'] = data
        f.seek(0)
        f.truncate()
        f.write(json.dumps(_tmp1, ensure_ascii=False, indent=4,
                           sort_keys=True))


def DelorRe_TX(lolpath, model="GET"):
    import os, json, shutil
    t = ["rcp-fe-rpcs", "rcp-fe-gdp-live"]
    _js = os.path.join(lolpath, "LeagueClient/Plugins/plugin-manifest.json")
    backjs = os.path.join(lolpath, "LeagueClient/Plugins/backup.json")
    if model == "SET":
        flag = True
        with open(_js, "r+", encoding="utf-8") as f:
            data = json.load(f)
            p = 0
            i = 0
            while True:
                if i == len(data['plugins']):
                    break
                item = data['plugins'][i]
                if item['name'] in t:
                    data['plugins'].remove(item)
                    i -= 1
                    p += 1
                    if p == 2:
                        shutil.copy(_js, backjs)
                        break
                    flag = False
                i += 1
            f.seek(0)
            f.truncate()
            f.write(
                json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True))
        if flag:
            os.remove(_js)
            shutil.copy(backjs, _js)
    elif model == "GET":
        i = 0
        with open(_js, "r+", encoding="utf-8") as f:
            data = json.load(f)
            for item in data['plugins']:
                if item['name'] in t:
                    i += 1
        return True if i != 0 else False
    pass