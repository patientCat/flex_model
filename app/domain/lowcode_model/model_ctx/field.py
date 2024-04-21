from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, TypedDict, List

from app.common.bizlogger import LOGGER
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


COLUMN_FORMAT_SET = {column_format.value for column_format in ColumnFormat.__members__.values()}


class ColumnType(Enum):
    NUMBER = "number"
    STRING = "string"
    BOOL = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    NULL = "null"


COLUMN_TYPE_SET = {column_type.value for column_type in ColumnType.__members__.values()}

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
    KEY_FORMAT = "format"
    KEY_TYPE = "type"

    def __init__(self, key, json_val):
        self.key = key
        self.json_val = json_val

    @property
    def name(self) -> str:
        return self.key

    @property
    def format(self) -> str:
        _format = self.json_val.get(self.KEY_FORMAT, "")
        if _format not in COLUMN_FORMAT_SET:
            LOGGER.warning(f"invalid format for '{_format}'")
        return _format

    @property
    def type(self) -> Optional[ColumnType]:
        _type = self.json_val.get(self.KEY_TYPE, "")
        if _type not in COLUMN_TYPE_SET:
            LOGGER.warning(f"invalid type for '{_type}'")
            return None
        return ColumnType(_type)

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
