from httpx import get
from json import dumps

if __name__ == "__main__":
    uri = "https://gitee.com/ASTWY/lcufix-tool/raw/master/version.json"
    resp = get(uri)
    if resp.status_code == 200:
        data = resp.json()
        result = {}
        for item in data["data"]:
            result[item["class"]] = []
        for item in data["data"]:
            # 向result中添加数据,将item中的class键值对移除
            key = item["class"]
            item.pop("class")
            result[key].append(item)
            pass

    print(dumps(result, indent=4, ensure_ascii=False))

    pass
