from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, TypedDict, List

from app.common.error import BizException, ErrorCode


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

    @abstractmethod
    def key(self):
        pass

    @abstractmethod
    def json_val(self):
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


class JsonSchemaDict(TypedDict, total=False):
    type: str
    format: str
    name: str
    description: str
    xRelation: dict
    maxLength: int
    minLength: int


class SchemaColumn(MetaColumn):
    def __init__(self, key: str, json_val: JsonSchemaDict):
        self.__key: str = key
        self.__json_val: JsonSchemaDict = json_val

    @property
    def name(self) -> str:
        return self.__json_val.get("name", "")

    @property
    def format(self) -> str:
        _format = self.__json_val.get("format", "")
        return _format

    @property
    def type(self) -> Optional[ColumnType]:
        _type = self.__json_val.get("type", "")
        return ColumnType(_type)

    @property
    def key(self) -> str:
        return self.__key

    @property
    def json_val(self) -> JsonSchemaDict:
        return self.__json_val

    def is_relation(self) -> bool:
        if self.format in RELATION_FORMAT_LIST:
            return True
        else:
            return False

    def get_relation(self) -> Optional[RelationInfo]:
        if not self.is_relation():
            return None
        x_relation = self.__json_val.get("xRelation")
        if x_relation is None:
            return None
        return x_relation

    def __str__(self) -> str:
        return f"SchemaColumn(value={self.__dict__})"

    def __repr__(self) -> str:
        return self.__str__()


class SchemaColumnFactory:
    @staticmethod
    def create_column(key: str, json_val: JsonSchemaDict) -> SchemaColumn:
        name = json_val.get("name", "")
        if name == "":
            raise BizException(ErrorCode.InvalidParameter, f"key={key}, json_val={json_val}, name is required")
        format_v = json_val.get("format", "")
        if format_v == "":
            raise BizException(ErrorCode.InvalidParameter, f"key={key}, json_val={json_val}, format is required")
        if format_v not in COLUMN_FORMAT_SET:
            raise BizException(ErrorCode.InvalidParameter, f"key={key}, json_val={json_val}, format is invalid")
        type_v = json_val.get("type", "")
        if type_v == "":
            raise BizException(ErrorCode.InvalidParameter, f"key={key}, json_val={json_val}, type is required")
        if type_v not in COLUMN_TYPE_SET:
            raise BizException(ErrorCode.InvalidParameter, f"type={key}, json_val={json_val}, type is invalid")
        return SchemaColumn(key, json_val)

    @staticmethod
    def create_column_list(json_schema: dict) -> List[SchemaColumn]:
        properties = json_schema.get("properties")
        column_list = []
        for key, json_val in properties.items():
            column = SchemaColumnFactory.create_column(key, json_val)
            column_list.append(column)
        return column_list
