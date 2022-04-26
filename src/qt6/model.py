class WAD_Info:
    def __init__(self, **kwargs):
        self.name: str = kwargs.get("name")
        self.path: str = kwargs.get("path")
        self.class_: str = kwargs.get("class")
        self.note: str = kwargs.get("note")
        self.md5: str = kwargs.get("md5")
        self.type: str = kwargs.get("type")
        self.orgin_key: str = kwargs.get("orginKey")
        self.orgin_value: str = kwargs.get("orginValue")
        self.__dict__.update(kwargs)


# 服务器数据
class Server_Info:
    def __init__(self, **kwargs):
        self.ver: str = kwargs.get("ver")
        self.host: str = kwargs.get("host")
        self.msgContorl: bool = kwargs.get("msgContorl")
        self.msg: str = kwargs.get("msg")
        # 将传入的数据中的data转化为元素类型为WADinfo的列表
        self.data: list[WAD_Info] = [WAD_Info(**item) for item in kwargs.get("data")]


if __name__ == "__main__":
    import httpx

    resp = httpx.get("https://gitee.com/ASTWY/lcufix-tool/raw/master/version.json")
    if resp.status_code == 200:
        info = Server_Info(**resp.json())
        print(info.data[0].name)
        print(info.ver)
