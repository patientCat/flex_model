from dataclasses import dataclass
from typing import Dict, List

from app.common.error import ErrorCode, BizException
from app.service.model_domain.metadata import field


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


@dataclass
class DatabaseIdentity:
    database_name: str
    type: str


class ModelContext:
    def __init__(self, model_name: ModelNameCtx, database_identity: DatabaseIdentity, key_2_schema_column_map: dict):
        self.model_name: ModelNameCtx = model_name
        self.database_identity: DatabaseIdentity = database_identity
        self.key_2_schema_column_map: Dict[str, field.SchemaColumn] = key_2_schema_column_map

    @staticmethod
    def create_from_schema(json_schema: dict):
        model_name = json_schema.get("x-model-name")
        if model_name is None or model_name == "":
            raise BizException(ErrorCode.InternalError, "x-model-name not set")
        namespace = json_schema.get("x-namespace")
        model_name = ModelNameCtx(model_name, namespace)
        database_name = json_schema.get("x-database-name")
        if database_name is None or database_name == "":
            raise BizException(ErrorCode.InternalError, "x-database-name not set")
        database_id = DatabaseIdentity(database_name, "mongo")

        properties = json_schema.get("properties")
        key_2_schema_column = {}
        for k, v in properties.items():
            column = field.SchemaColumn(k, v)
            key_2_schema_column[k] = column
        return ModelContext(model_name=model_name, database_identity=database_id,
                            key_2_schema_column_map=key_2_schema_column)

    def schema_column_list(self) -> List[field.SchemaColumn]:
        # return value of key_2_schema_column_map
        return self.key_2_schema_column_map.values()

    def schema_column(self, column_name) -> field.SchemaColumn:
        return self.key_2_schema_column_map.get(column_name, None)
