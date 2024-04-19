from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, TypedDict, List

import loguru

from app.common.error import BizException, ErrorCode
from app.domain.lowcode_model.model_ctx import constant


class ColumnFormat(Enum):
    """
    xShortText
    maxLength less than 256
    """
    SHORT_TEXT = "xShortText"
    """
    xLongText
    maxLength less than 512K
    """
    LONG_TEXT = "xLongText"
    NUMBER = "xNumber"
    JSON = "xJson"
    EMAIL = "email"
    MANY_TO_ONE = "xManyToOne"
    ONE_TO_MANY = "xOneToMany"
    MANY_TO_MANY = "xManyToMany"

    def get_enum_value(self):
        return getattr(self, "_enum_value", None)


class ColumnType(Enum):
    NUMBER = "number"
    STRING = "string"
    BOOL = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    NULL = "null"


RELATION_FORMAT_LIST: List[str] = [ColumnFormat.MANY_TO_ONE.value,
                                   ColumnFormat.MANY_TO_MANY.value,
                                   ColumnFormat.ONE_TO_MANY.value]


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


class RelationInfo(TypedDict, total=False):
    """
    {
      "field": "userId",
      "relatedField": "_id",
      "relatedModelName":"user"
    }
    """
    field: str
    relatedField: str
    relatedModelName: str


class SchemaColumn(MetaColumn):
    def __init__(self, key, json_val):
        self.key = key
        self.json_val = json_val

    @property
    def name(self) -> str:
        return self.key

    @property
    def format(self) -> str:
        _format = self.json_val.get(constant.SCHEMA_KEYS["format"], "")
        if _format is None or _format == "":
            return ""
        try:
            return ColumnFormat(_format).value
        except ValueError:
            loguru.logger.error(f"Invalid format for {_format}")
            return _format

    @property
    def type(self) -> ColumnType:
        _type = self.json_val.get(constant.SCHEMA_KEYS["type"], "")
        try:
            return ColumnType(_type)
        except ValueError:
            raise BizException(ErrorCode.InvalidParameter, f"Invalid type for {_type}")

    def is_relation(self) -> bool:
        if self.format in RELATION_FORMAT_LIST:
            return True
        else:
            return False

    def get_relation(self) -> Optional[RelationInfo]:
        if not self.is_relation():
            return None
        x_relation = self.json_val.get(constant.SCHEMA_KEYS["xRelation"])
        if x_relation is None:
            return None
        return x_relation

    def __str__(self) -> str:
        return f"SchemaColumn(value={self.__dict__})"

    def __repr__(self) -> str:
        return self.__str__()
