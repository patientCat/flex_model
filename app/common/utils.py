import json


class CustomNamespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, item):
        return self.__dict__.get(item, None)  # 返回None如果键不存在


def serialize_instance(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        raise TypeError(repr(obj) + " is not JSON serializable")


def toJSON(obj, serializer=None):
    if obj is None:
        return None
    if serializer is None:
        return json.dumps(
            obj,
            default=lambda o: o.__dict__,
        )
    else:
        return json.dumps(
            obj,
            default=serializer
        )
