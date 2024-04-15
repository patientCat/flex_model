from abc import ABC, abstractmethod
from enum import Enum

from app.common.error import BizException, ErrorCode
from app.domain.lowcode_model.model_ctx import constant


class ColumnFormat(Enum):
    """
    x-short-text
    maxLength less than 256
    """
    SHORT_TEXT = "x-short-text"
    """
    x-long-text
    maxLength less than 512K
    """
    LONG_TEXT = "x-long-text"
    NUMBER = "x-number"
    JSON = "x-json"
    MANY_TO_ONE = "x-many-to-one"
    ONE_TO_MANY = "x-one-to-many"
    MANY_TO_MANY = "x-many-to-many"

    def get_enum_value(self):
        return getattr(self, "_enum_value", None)


class ColumnType(Enum):
    NUMBER = "number"
    STRING = "string"
    BOOL = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    NULL = "null"


RELATION_FORMAT_LIST = [ColumnFormat.MANY_TO_ONE, ColumnFormat.MANY_TO_MANY, ColumnFormat.ONE_TO_MANY]


class MetaColumn(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def format(self):
        pass

    @abstractmethod
    def type(self):
        pass


class SchemaColumn(MetaColumn):
    def __init__(self, key, json_val):
        self.key = key
        self.json_val = json_val

    @property
    def name(self) -> str:
        return self.key

    @property
    def format(self) -> ColumnFormat:
        _format = self.json_val.get(constant.SCHEMA_KEYS["FORMAT"], "")
        try:
            return ColumnFormat(_format)
        except ValueError:
            raise BizException(ErrorCode.InvalidParameter, f"Invalid format for {_format}")

    @property
    def type(self) -> ColumnType:
        _type = self.json_val.get(constant.SCHEMA_KEYS["TYPE"], "")
        try:
            return ColumnType(_type)
        except ValueError:
            raise BizException(ErrorCode.InvalidParameter, f"Invalid type for {_type}")

    def is_relation(self) -> bool:
        return self.format in RELATION_FORMAT_LIST
