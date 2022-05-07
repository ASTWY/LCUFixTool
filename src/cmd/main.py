import json
import os
import sys
import time
from datetime import time

from rich.console import Console
from rich.progress import track
from rich.table import Table

from pathlib import Path

print(Path("~\Documents\LCUFixTool"))

from model import *

cfg = GetConfig()
config = {}
if __name__ == "__main__":
    col = Console()
    # col.log('欢迎使用LCUFixTool')
    # 声明
    col.print("[blod]使用须知")
    col.print("所有修改方法思路均由[cyan]B站@ZYXeeker[/cyan][red]原创![/red]")
    col.print("由[cyan]Valhir丨B站艾斯托维亚&蓝星A11[/cyan]提[green]供技术支持！[/green]")
    col.print("[red]只作个人学习研究用途公开，不承担任何责任。[/red]")
    col.print("\n")

    cfg_path = os.path.expanduser("~\Documents\LCUFixTool")
    if not os.path.exists(cfg_path):
        os.mkdir(cfg_path)
    _skip = False
    if os.path.exists(os.path.join(cfg_path, "config.json")):
        config = json.load(open(os.path.join(cfg_path, "config.json"), "r"))
        if config.get("skip") == False:
            _skip = True
    if not _skip:
        for i in track(
            range(5),
            description="Waiting...",
        ):
            time.sleep(1)
        col.clear()

    # 获取游戏路径
    _path = ""
    if os.path.exists(os.path.join(cfg_path, "config.json")):
        config = json.load(open(os.path.join(cfg_path, "config.json"), "r"))
        _path = config.get("lol")
    while True:
        if not os.path.exists(os.path.join(_path, "LeagueClient\\Plugins")):
            _path = GetLOLPath()
        else:
            if config.get("lol") != _path:
                config["lol"] = _path
                with open(
                    os.path.join(cfg_path, "config.json"), "w+", encoding="utf-8"
                ) as f:
                    f.seek(0)
                    f.truncate()
                    f.write(
                        json.dumps(config, ensure_ascii=False, indent=4, sort_keys=True)
                    )
            break

    # 检查版本是否支持
    _ver = getFileVersion(os.path.join(_path, "Game\\League of Legends.exe"))
    if _ver != cfg["ver"]:
        col.print(
            "[bold cyan]{}[/bold cyan][bold red]暂不支持[/bold red]，请耐心等待更新".format(_ver)
        )
        os.system("pause")
    else:
        while True:
            # 功能列表
            table = Table(
                show_header=True, header_style="bold magenta", show_lines=True
            )
            table.add_column("序号")
            table.add_column("状态")
            table.add_column("功能类别")
            table.add_column("备注")
            _classDict = {}
            i = 1
            for item in cfg["data"]:
                if item["class"] not in _classDict:
                    _classDict[item["class"]] = {"num": i, "data": []}
                    i += 1
                _classDict[item["class"]]["data"].append(item)
            for item in _classDict:
                _tmpList = _classDict[item]
                _state = True
                _notes = ""
                for p in _tmpList["data"]:
                    _tstate = Set_or_Get_wad_state(lolpath=_path, wadinfo=p)
                    if not _tstate:
                        for _titem in _tmpList["data"]:
                            Set_or_Get_wad_state(
                                lolpath=_path, wadinfo=_titem, model="DEL"
                            )
                    _state = _state and _tstate
                    _notes = p["note"]
                pass
                table.add_row(
                    str(_tmpList["num"]),
                    str("[green]√\t[/green]" if _state else "[red]×\t[/red]"),
                    item,
                    _notes,
                )
            # 特殊功能
            table.add_row(
                str(i),
                str(
                    "[green]√\t[/green]"
                    if (not DelorRe_TX(_path))
                    else "[red]×\t[/red]"
                ),
                "净化客户端",
                "移除客户端内TX插件,前往[bold cyan]https://astwy.top/lol/xgzy/lcufix.html[/bold cyan]了解详情",
            )
            if cfg.get("msgContorl"):
                col.print("[blod]公告")
                col.print(cfg.get("msg"))
            col.print("英雄联盟路径:[bold cyan]{}[/bold cyan]".format(_path))
            col.print(table)
            # 获取要配置的功能id
            try:
                id = int(col.input("请输入要配置的功能[bold cyan]序号[/bold cyan]并按回车\n"))
                if id == 688:
                    if os.path.exists(os.path.join(cfg_path, "config.json")):
                        os.remove(os.path.join(cfg_path, "config.json"))
                        col.print("路径配置已清除，软件即将自动退出")
                        time.sleep(1)
                        sys.exit()
                if not (id > 0 and id <= i):
                    continue
                for item in _classDict:
                    if id != _classDict[item]["num"]:
                        continue
                    _tmpList = _classDict[item]["data"]
                    for p in _tmpList:
                        Set_or_Get_wad_state(
                            _path, p, model="SET", downhost=cfg["host"]
                        )
                        pass
                # 净化客户端
                if id == i:
                    DelorRe_TX(_path, model="SET")
                    col.clear()
                col.clear()
                pass
            except ValueError:
                col.print("[red]请输入正确的值!")
                time.sleep(1)
                col.clear()
