import json
import re
import sqlite3
from typing import Dict, List, Optional

import loguru
import sqlalchemy

from app.common.error import ErrorCode, BizException, EzErrorCodeEnum
from app.domain.lowcode_model.model_ctx import field
from app.domain.lowcode_model.model_ctx.json_schema import JsonSchemaChecker
from app.repo.interface import ModelRepo
from app.repo.po import ModelPO

# ModelNameCtx 模型标识上下文
NAME_PATTERN = r"^[a-zA-Z][a-zA-Z0-9-_]*$"
ERROR_MATCH_NAME_PATTERN = "Name must start with letters, and it can only contain letters , numbers, '-', '_'"


def check_name(name: str) -> bool:
    # 使用 re.match() 函数检查字符串是否符合正则表达式模式
    if re.match(NAME_PATTERN, name):
        return True
    else:
        return False


class ModelNameContext:
    def __init__(self, *, name: str, project_id: str, ns: str = None):
        self.namespace = ns
        self.name = name
        self.project_id = project_id

    @staticmethod
    def validate_and_create(*, name: str, project_id: str, ns: str = None) -> "ModelNameContext":
        if not check_name(name):
            raise BizException(ErrorCode.InvalidParameter, ERROR_MATCH_NAME_PATTERN)
        return ModelNameContext(name=name, project_id=project_id, ns=ns)

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
        return {"json_schema": self.__json_schema, "autotest": True}

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
        if self.__column_list is None:
            return []
        return self.__column_list

    @property
    def relation_column_list(self) -> List[field.SchemaColumn]:
        if self.column_list is None:
            return []
        return [column for column in self.column_list if column.is_relation]

    def validate_on_create(self, data: Dict):
        if data is None:
            return
        validation_result = self.__json_schema_checker.validate_on_create(data)
        if validation_result.is_valid:
            return
        else:
            raise BizException(ErrorCode.InvalidParameter, validation_result.error_message)

    def validate_on_create_many(self, data: list):
        if data is None:
            return
        validation_result = self.__json_schema_checker.validate_on_create_many(data)
        loguru.logger.info(f"Validation result: {validation_result}")
        if validation_result.is_valid:
            return
        else:
            raise BizException(ErrorCode.InvalidParameter, validation_result.error_message)

    def validate_on_update(self, param: Dict):
        data = param.get("data")
        if data is None:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound, arg_list=["data", '[{"foo":"bar"}]'])
        validation_result = self.__json_schema_checker.validate_on_update(data)
        if validation_result.is_valid:
            return
        else:
            raise BizException(ErrorCode.InvalidParameter, validation_result.error_message)


class MetadataContextPool:
    def __init__(self, model_repo: ModelRepo):
        self.__metadata_context_pool: Dict[str, MetadataContext] = dict()
        self.__model_repo = model_repo

    def get_by_name(self, project_id, name) -> Optional[MetadataContext]:
        if name in self.__metadata_context_pool:
            return self.__metadata_context_pool[name]

        model: ModelPO = self.__model_repo.get_model_by_name(project_id=project_id, model_name=name)
        if model is None:
            raise BizException(
                code=ErrorCode.InvalidParameter,
                message=f"get_model_by_name_is_none_project_id={project_id}_model_name={name}"
            )
        if model.schema is None:
            raise BizException(
                code=ErrorCode.InvalidParameter,
                message=f"model_schema_is_none_project_id={project_id}_model_name={name}"
            )
        json_schema = json.loads(model.schema)
        metadata_ctx = MetadataContext(json_schema=json_schema)
        self.__metadata_context_pool[name] = metadata_ctx
        return metadata_ctx

    def create(self, model_po: ModelPO):
        self.__model_repo.create_model(model_po)

    def add(self, name: str, value: ModelPO):
        json_schema = json.loads(value.schema)
        self.__metadata_context_pool[name] = MetadataContext(json_schema=json_schema)


def check_schema(schema: dict) -> bool:
    if "properties" not in schema:
        raise ValueError("schema must contain 'properties'")
    if "type" not in schema:
        raise ValueError("schema must contain 'type'")


class ModelContext:
    def __init__(self, model_name_ctx: ModelNameContext,
                 metadata_ctx_pool: MetadataContextPool):
        self.__model_name_ctx: ModelNameContext = model_name_ctx
        self.__metadata_ctx_pool = metadata_ctx_pool

    @staticmethod
    def create(model_name_ctx: ModelNameContext, model_repo: ModelRepo) -> "ModelContext":
        pool = MetadataContextPool(model_repo=model_repo)
        return ModelContext(model_name_ctx, pool)

    @property
    def model_name_ctx(self) -> ModelNameContext:
        return self.__model_name_ctx

    def get_master_metadata_ctx(self) -> MetadataContext:
        name = self.__model_name_ctx.name
        return self.__metadata_ctx_pool.get_by_name(self.__model_name_ctx.project_id, name)

    def get_metadata_ctx_by_name(self, model_name: str) -> MetadataContext:
        return self.__metadata_ctx_pool.get_by_name(self.__model_name_ctx.project_id, model_name)

    def create_metadata_ctx(self, *, schema):
        project_id = self.__model_name_ctx.project_id
        model_name = self.__model_name_ctx.name
        json_schema = json.dumps(schema)
        model_po: ModelPO = ModelPO(model_name=self.__model_name_ctx.name,
                                    project_id=self.__model_name_ctx.project_id,
                                    schema=json_schema
                                    )
        try:
            check_schema(schema)
        except Exception as e:
            raise BizException(ErrorCode.InvalidParameter, f"{e}")

        try:
            self.__metadata_ctx_pool.create(model_po=model_po)
        except sqlalchemy.exc.IntegrityError as e:
            if isinstance(e, sqlalchemy.exc.IntegrityError):
                raise BizException(ErrorCode.InvalidParameter,
                                   f"project='{project_id}', model_name='{model_name}' already exists")
            raise e
        self.__metadata_ctx_pool.add(name=self.__model_name_ctx.name, value=model_po)
