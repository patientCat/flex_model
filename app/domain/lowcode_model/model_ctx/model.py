import json
import re
from typing import Dict, List, Optional

import sqlalchemy

from app.common.bizlogger import LOGGER
from app.common.error import ErrorCode, BizException, EzErrorCodeEnum
from app.domain.lowcode_model.model_ctx.column import SchemaColumn, SchemaColumnFactory, ColumnFormat
from app.domain.lowcode_model.model_ctx.json_schema import JsonSchemaChecker
from app.domain.lowcode_model.model_ctx.model_validator import ColumnValidatorFactory
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
        self.__column_list: List[SchemaColumn] = MetadataContext.get_column_list_from_schema(json_schema)
        self.__json_schema_checker: JsonSchemaChecker = JsonSchemaChecker(json_schema=json_schema)

    @property
    def __dict__(self) -> dict:
        return {"json_schema": self.__json_schema, "autotest": True}

    @property
    def json_schema(self) -> dict:
        return self.__json_schema

    @staticmethod
    def get_column_list_from_schema(json_schema: dict) -> list:
        properties = json_schema.get("properties")
        column_list = []
        for k, v in properties.items():
            column = SchemaColumn(k, v)
            column_list.append(column)
        return column_list

    @property
    def column_list(self) -> List[SchemaColumn]:
        if self.__column_list is None:
            return []
        return self.__column_list

    @property
    def relation_column_list(self) -> List[SchemaColumn]:
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
        LOGGER.info(f"Validation result: {validation_result}")
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

    @staticmethod
    def compose_schema_by_add(*, schema: dict, column_list: List[SchemaColumn]) -> dict:
        json_schema = schema.copy()
        return SchemaColumnFactory.compose_schema_by_add(schema=json_schema, column_list=column_list)

    @staticmethod
    def compose_schema_by_remove(*, schema: dict, column_name_list: List[str]) -> dict:
        json_schema = schema.copy()
        return SchemaColumnFactory.compose_schema_by_remove(schema=json_schema, column_name_list=column_name_list)


class MetadataContextDomain:
    def __init__(self, model_repo: ModelRepo):
        self.__model_repo = model_repo
        # todo 加入缓存

    def get_by_name(self, project_id, name) -> Optional[MetadataContext]:
        # todo 从缓存中取
        model: ModelPO = self.__model_repo.get_model_by_name(project_id=project_id, model_name=name)
        if model is None:
            raise BizException(
                code=ErrorCode.InvalidParameter,
                message=f"get_model_by_name_is_none_project_id='{project_id}'_model_name='{name}'"
            )
        if model.schema is None:
            raise BizException(
                code=ErrorCode.InvalidParameter,
                message=f"model_schema_is_none_project_id='{project_id}'_model_name='{name}'"
            )
        json_schema = json.loads(model.schema)
        metadata_ctx = MetadataContext(json_schema=json_schema)
        return metadata_ctx

    def create(self, model_po: ModelPO):
        self.__model_repo.create_model(model_po)
        # todo 加入缓存

    def update_schema(self, *, project_id, mode_name, schema):
        schema_string = json.dumps(schema)
        self.__model_repo.update_schema(project_id=project_id, model_name=mode_name, schema=schema_string)


def check_schema(schema: dict) -> None:
    if "properties" not in schema:
        raise ValueError("schema must contain 'properties'")
    if "type" not in schema:
        raise ValueError("schema must contain 'type'")


class ModelContext:
    def __init__(self, model_name_ctx: ModelNameContext,
                 metadata_ctx_domain: MetadataContextDomain):
        self.__model_name_ctx: ModelNameContext = model_name_ctx
        self.__metadata_ctx_domain = metadata_ctx_domain
        self.__column_validator_factory = ColumnValidatorFactory()

    @staticmethod
    def create(model_name_ctx: ModelNameContext, model_repo: ModelRepo) -> "ModelContext":
        pool = MetadataContextDomain(model_repo=model_repo)
        return ModelContext(model_name_ctx, pool)

    @property
    def model_name_ctx(self) -> ModelNameContext:
        return self.__model_name_ctx

    def get_master_metadata_ctx(self) -> MetadataContext:
        name = self.__model_name_ctx.name
        return self.get_metadata_ctx_by_name(name)

    def get_metadata_ctx_by_name(self, model_name: str) -> MetadataContext:
        return self.__metadata_ctx_domain.get_by_name(self.__model_name_ctx.project_id, model_name)

    def create_metadata_ctx(self, *, schema: dict, db_type: str):
        project_id = self.__model_name_ctx.project_id
        model_name = self.__model_name_ctx.name

        try:
            check_schema(schema)
        except Exception as e:
            raise BizException(ErrorCode.InvalidParameter, f"{e}")

        # 验证schema的每一列，然后重新填充
        schema = self.validate_and_fill_schema(schema)
        try:
            str_schema = json.dumps(schema)
            model_po: ModelPO = ModelPO(model_name=self.__model_name_ctx.name,
                                        project_id=self.__model_name_ctx.project_id,
                                        schema=str_schema
                                        )
            self.__metadata_ctx_domain.create(model_po=model_po)
        except sqlalchemy.exc.IntegrityError as e:
            if isinstance(e, sqlalchemy.exc.IntegrityError):
                raise BizException(ErrorCode.InvalidParameter,
                                   f"project='{project_id}', model_name='{model_name}' already exists")
            raise e

        if db_type == 'mysql':
            # do_create_table
            pass

    def validate_and_fill_schema(self, schema):
        column_list = SchemaColumnFactory.create_column_list(schema)
        for column in column_list:
            column_format: ColumnFormat = column.column_format
            column_validator = self.__column_validator_factory.create_validator(column_format)
            if column_validator is not None:
                column_validator.validate_and_fill(column)
        schema = SchemaColumnFactory.compose_schema_by_add(schema=schema, column_list=column_list)
        return schema

    def add_column(self, add_column_list: List[dict]):

        metadata_ctx = self.get_master_metadata_ctx()
        column_list = metadata_ctx.column_list
        existed_column_set = set([column.name for column in column_list])
        new_column_list = []
        for add_column in add_column_list:
            print(f"add_column ={add_column}, {add_column_list}")
            add_column_name = add_column.get('name')
            if add_column_name in existed_column_set:
                raise BizException(ErrorCode.InvalidParameter,
                                   f"column '{add_column_name}' already exists in model '{self.__model_name_ctx.name}'")
            new_column = SchemaColumnFactory.create_column(add_column.get('name'), add_column)
            new_column_list.append(new_column)

        new_schema = MetadataContext.compose_schema_by_add(schema=metadata_ctx.json_schema, column_list=new_column_list)
        model_name_ctx = self.__model_name_ctx
        self.__metadata_ctx_domain.update_schema(
            project_id=model_name_ctx.project_id,
            mode_name=model_name_ctx.name,
            schema=new_schema)

    def delete_column(self, column_name_list: List[str]):
        metadata_ctx = self.get_master_metadata_ctx()

        new_schema = MetadataContext.compose_schema_by_remove(schema=metadata_ctx.json_schema,
                                                              column_name_list=column_name_list)
        model_name_ctx = self.__model_name_ctx
        self.__metadata_ctx_domain.update_schema(
            project_id=model_name_ctx.project_id,
            mode_name=model_name_ctx.name,
            schema=new_schema)
