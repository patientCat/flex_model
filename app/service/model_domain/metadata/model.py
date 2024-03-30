from app.service.model_domain.metadata import field
from typing import Dict, List


class ModelName:
    def __init__(self, table_name, namespace):
        self.table_name = table_name
        self.namespace = namespace


class ModelContext:
    def __init__(self, model_name: ModelName, key_2_schema_column_map: dict):
        self.model_name: ModelName = model_name
        self.key_2_schema_column_map: Dict[str, field.SchemaColumn] = key_2_schema_column_map

    @staticmethod
    def create_from_schema(json_schema: dict):
        model_name = json_schema.get("x-model-name")
        namespace = json_schema.get("x-namespace")
        model_name = ModelName(model_name, namespace)

        properties = json_schema.get("properties")
        key_2_schema_column = {}
        for k, v in properties.items():
            column = field.SchemaColumn(k, v)
            key_2_schema_column[k] = column
        return ModelContext(model_name=model_name, key_2_schema_column_map=key_2_schema_column)

    def schema_column_list(self) -> List[field.SchemaColumn]:
        # return value of key_2_schema_column_map
        return self.key_2_schema_column_map.values()

    def schema_column(self, column_name) -> field.SchemaColumn:
        return self.key_2_schema_column_map.get(column_name, None)
