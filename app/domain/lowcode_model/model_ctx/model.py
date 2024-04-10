from dataclasses import dataclass
from typing import Dict, List

from app.common.error import ErrorCode, BizException
from app.domain.database_ctx.context import DatabaseIdentity
from app.domain.lowcode_model.model_ctx import field


# ModelNameCtx 模型标识上下文
class ModelNameCtx:
    def __init__(self, name: str, ns: str = None):
        self.namespace = ns
        self.name = name

    @property
    def collection_name(self) -> str:
        if self.namespace is None or self.namespace == "":
            return self.name
        else:
            return f"{self.namespace}_{self.name}"


class MetadataContext:
    def __init__(self, column_list: List[field.SchemaColumn]):
        self.__column_list: List[field.SchemaColumn] = column_list

    @staticmethod
    def create_from_schema(json_schema: dict) -> "MetadataContext":
        properties = json_schema.get("properties")
        column_list = []
        for k, v in properties.items():
            column = field.SchemaColumn(k, v)
            column_list.append(column)

        return MetadataContext(column_list)

    @property
    def column_list(self) -> List[field.SchemaColumn]:
        return self.__column_list


class ModelContext:
    def __init__(self, model_name_ctx: ModelNameCtx, database_identity: DatabaseIdentity,
                 metadata_ctx: MetadataContext):
        self.__model_name_ctx: ModelNameCtx = model_name_ctx
        self.__database_identity: DatabaseIdentity = database_identity
        self.__metadata_ctx = metadata_ctx

    @staticmethod
    def create_from_schema(json_schema: dict):
        model_name = json_schema.get("x-model-name")
        if model_name is None or model_name == "":
            raise BizException(ErrorCode.InternalError, "x-model-name not set")
        namespace = json_schema.get("x-namespace")
        model_name_ctx = ModelNameCtx(model_name, namespace)
        database_name = json_schema.get("x-database-name")
        if database_name is None or database_name == "":
            raise BizException(ErrorCode.InternalError, "x-database-name not set")
        database_id = DatabaseIdentity(database_name, "mongo")

        properties = json_schema.get("properties")
        column_list = []
        for k, v in properties.items():
            column = field.SchemaColumn(k, v)
            column_list.append(column)

        metadata_ctx = MetadataContext(column_list)
        return ModelContext(model_name_ctx=model_name, database_identity=database_id,
                            metadata_ctx=metadata_ctx)

    @property
    def metadata_ctx(self) -> MetadataContext:
        # return value of key_2_schema_column_map
        return self.__metadata_ctx

    @property
    def database_identity(self) -> DatabaseIdentity:
        return self.__database_identity
