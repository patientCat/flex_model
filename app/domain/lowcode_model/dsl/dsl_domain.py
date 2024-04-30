from typing import List

from app.domain.lowcode_model.model_ctx.column import SchemaColumn


class CreateTableDomain:
    def __init__(self):
        self.__column_list: List[SchemaColumn] = None


class DdlDomainFactory:
    def create_table_domain(self):
        pass
