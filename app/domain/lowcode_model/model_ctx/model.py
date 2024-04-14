from typing import Dict, List

from app.common.error import ErrorCode, BizException
from app.domain.lowcode_model.model_ctx import field
from app.domain.lowcode_model.model_ctx.json_schema import JsonSchemaChecker
from app.repo.interface import ModelRepo


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
        data: List = param.get("data")
        print(data)
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


class MetadataContextPool:
    def __init__(self, model_repo: ModelRepo):
        self.__metadata_context_pool = dict()
        self.__model_repo = model_repo

    def get_by_name(self, project_id, name) -> MetadataContext:
        if name in self.__metadata_context_pool:
            return self.__metadata_context_pool[name]
        else:
            model = self.__model_repo.get_model_by_name(project_id=project_id, model_name=name)
            # TODO 处理缓存
            return model


class ModelContext:
    def __init__(self, model_name_ctx: ModelNameContext,
                 metadata_ctx_pool: MetadataContextPool):
        self.__model_name_ctx: ModelNameContext = model_name_ctx
        self.__metadata_ctx_pool = metadata_ctx_pool

    @property
    def model_name_ctx(self) -> ModelNameContext:
        return self.__model_name_ctx

    def metadata_ctx(self, project_id) -> MetadataContext:
        name = self.__model_name_ctx.name
        return self.__metadata_ctx_pool.get_by_name(project_id, name)

    def get_metadata_ctx_by_name(self, project_id, model_name: str) -> MetadataContext:
        return self.__metadata_ctx_pool.get_by_name(project_id, model_name)
