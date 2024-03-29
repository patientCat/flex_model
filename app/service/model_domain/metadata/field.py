from abc import abstractmethod
import constant


class MetaColumn:
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def format(self):
        pass

    @abstractmethod
    def type(self):
        pass


class ColumnFormat:
    # 长度不超过256，用来存放一些标识，可以建立索引
    FORMAT_SHORT_TEXT = "x-short-text"
    # 存放长文本数据，不可以建立索引
    FORMAT_LONG_TEXT = "x-long-text"
    # 普通数字
    FORMAT_NUMBER = "x-number"
    # 自定义json字段, 自己负责校验
    FORMAT_JSON = "x-json"
    # 多对一关联关系
    FORMAT_MANY_TO_ONE = "x-many-to-one"
    # 一对多关联关系
    FORMAT_ONE_TO_MANY = "x-one-to-many"
    # 多对多关联关系
    FORMAT_MANY_TO_MANY = "x-many-to-many"

    def __init__(self, key_format: str):
        self.key_format = key_format

    def is_short_text(self) -> bool:
        return self.key_format == ColumnFormat.FORMAT_SHORT_TEXT

    def is_long_text(self) -> bool:
        return self.key_format == ColumnFormat.FORMAT_LONG_TEXT

    def is_number(self) -> bool:
        return self.key_format == ColumnFormat.FORMAT_NUMBER

    def is_json(self) -> bool:
        return self.key_format == ColumnFormat.FORMAT_JSON

    def is_many_to_one(self) -> bool:
        return self.key_format == ColumnFormat.FORMAT_MANY_TO_ONE

    def is_one_to_many(self) -> bool:
        return self.key_format == ColumnFormat.FORMAT_ONE_TO_MANY

    def is_many_to_many(self) -> bool:
        return self.key_format == ColumnFormat.FORMAT_MANY_TO_MANY


class ColumnType:
    TYPE_NUMBER = "number"
    TYPE_STRING = "string"
    TYPE_BOOL = "boolean"
    TYPE_ARRAY = "array"
    TYPE_OBJECT = "object"
    TYPE_NULL = "null"

    def __init__(self, key_type):
        self.key_type = key_type

    def is_number(self) -> bool:
        return self.key_type == ColumnType.TYPE_NUMBER

    def is_string(self) -> bool:
        return self.key_type == ColumnType.TYPE_STRING

    def is_bool(self) -> bool:
        return self.key_type == ColumnType.TYPE_BOOL

    def is_array(self) -> bool:
        return self.key_type == ColumnType.TYPE_ARRAY

    def is_object(self) -> bool:
        return self.key_type == ColumnType.TYPE_OBJECT

    def is_null(self) -> bool:
        return self.key_type == ColumnType.TYPE_NULL


class SchemaColumn(MetaColumn):
    def __init__(self, key, json_val):
        super(SchemaColumn, self).__init__()
        self.key = key
        self.json_val = json_val

    def name(self):
        return self.key

    def format(self):
        return self.json_val.get(constant.SCHEMA_KEY_FORMAT, "")

    def type(self):
        return self.json_val.get(constant.SCHEMA_KEY_TYPE, "")
