from dataclasses import dataclass
from typing import Dict, List, Tuple

from app.common.error import ErrorCode, BizException
from app.domain.database_ctx.context import DatabaseIdentity
from app.domain.lowcode_model.model_ctx import field
from app.domain.lowcode_model.model_ctx.json_schema import JsonSchemaChecker


# ModelNameCtx 模型标识上下文
class ModelNameContext:
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
    def __init__(self, json_schema: dict):
        self.__json_schema = json_schema
        self.__column_list: List[field.SchemaColumn] = MetadataContext.get_column_list_from_schema(json_schema)
        self.__json_schema_checker: JsonSchemaChecker = JsonSchemaChecker(json_schema=json_schema)

    @property
    def __dict__(self) -> dict:
        return {"json_schema": self.__json_schema, "test": True}

    @staticmethod
    def get_column_list_from_schema(json_schema: dict) -> list:
        properties = json_schema.get("properties")
        column_list = []
        for k, v in properties.items():
            column = field.SchemaColumn(k, v)
            column_list.append(column)
        return column_list

    @property
    def column_list(self) -> List[field.SchemaColumn]:
        return self.__column_list

    def validate_on_create(self, param: Dict):
        data = param.get("data")
        validation_result = self.__json_schema_checker.validate_on_create(data)
        if validation_result.is_valid:
            return
        else:
            raise BizException(ErrorCode.InvalidParameter, validation_result.error_message)

    def validate_on_create_many(self, param: Dict):
        data: Dict = param.get("data")
        validation_result = self.__json_schema_checker.validate_on_create_many(data)
        if validation_result.is_valid:
            return
        else:
            raise BizException(ErrorCode.InvalidParameter, validation_result.error_message)

    def validate_on_update(self, param: Dict):
        data = param.get("data")
        validation_result = self.__json_schema_checker.validate_on_update(data)
        if validation_result.is_valid:
            return
        else:
            raise BizException(ErrorCode.InvalidParameter, validation_result.error_message)


class ModelContext:
    def __init__(self, model_name_ctx: ModelNameContext, database_identity: DatabaseIdentity,
                 metadata_ctx: MetadataContext):
        self.__model_name_ctx: ModelNameContext = model_name_ctx
        self.__database_identity: DatabaseIdentity = database_identity
        self.__metadata_ctx = metadata_ctx

    @staticmethod
    def create_from_schema(json_schema: dict):
        model_name = json_schema.get("x-model-name")
        if model_name is None or model_name == "":
            raise BizException(ErrorCode.InternalError, "x-model-name not set")
        model_name_ctx = ModelNameContext(model_name)
        database_name = json_schema.get("x-database-name")
        if database_name is None or database_name == "":
            raise BizException(ErrorCode.InternalError, "x-database-name not set")
        database_id = DatabaseIdentity(database_name, "mongo")

        metadata_ctx = MetadataContext(json_schema)
        return ModelContext(model_name_ctx=model_name_ctx, database_identity=database_id,
                            metadata_ctx=metadata_ctx)

    @property
    def model_name_ctx(self) -> ModelNameContext:
        return self.__model_name_ctx

    @property
    def metadata_ctx(self) -> MetadataContext:
        # return value of key_2_schema_column_map
        return self.__metadata_ctx

    @property
    def database_identity(self) -> DatabaseIdentity:
        return self.__database_identity
