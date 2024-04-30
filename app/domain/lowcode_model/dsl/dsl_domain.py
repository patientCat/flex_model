from typing import List

from app.domain.lowcode_model.model_ctx.column import SchemaColumn


class CreateTableDomain:
    def __init__(self):
        self.__column_list: List[SchemaColumn] = None


class DdlDomainFactory:
    def __init__(self, *, model_name: str, db_type: str):
        self.mode_name = model_name
        self.db_type = db_type

    def create_table_domain(self):
        pass
