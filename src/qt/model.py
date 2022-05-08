class WAD_Info:
    def __init__(self, **kwargs):
        self.name: str = kwargs.get("name")
        self.path: str = kwargs.get("path")
        self.note: str = kwargs.get("note")
        self.md5: str = kwargs.get("md5")
        self.type: str = kwargs.get("type")
        self.orgin_key: str = kwargs.get("orginKey")
        self.orgin_value: str = kwargs.get("orginValue")
        self.__dict__.update(kwargs)


# 服务器数据
class Server_Info(object):
    def __init__(self, **kwargs):
        self.ver: str = kwargs.get("ver")
        self.host: str = kwargs.get("host")
        self.msgContorl: bool = kwargs.get("msgContorl")
        self.msg: str = kwargs.get("msg")
        # 传入参数data中的项的子项转化为WAD_Info对象
        self.data: dict = {}
        for item in kwargs.get("data"):
            self.data[item] = [
                WAD_Info(**item) for item in kwargs.get("data").get(item)
            ]
