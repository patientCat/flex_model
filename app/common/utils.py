import json


class CustomNamespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, item):
        return self.__dict__.get(item, None)  # 返回None如果键不存在


def toJSON(obj):
    return json.dumps(
        obj,
        default=lambda o: o.__dict__,
        sort_keys=True,
        indent=4)
