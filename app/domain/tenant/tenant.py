from dataclasses import dataclass
from typing import Optional

from app.common import utils


@dataclass
class DatabaseInfo:
    db_url: str
    database_name: str
    user: str
    password: str


class TenantContext:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.database_map = {}

    @classmethod
    def create_from_json(cls, json_data: dict):
        namespace = utils.CustomNamespace(**json_data)
        tenant_ctx = TenantContext()
        tenant_ctx.name = namespace.name
        tenant_ctx.description = namespace.description
        if namespace.database_map is None:
            tenant_ctx.database_map = {}
        else:
            tenant_ctx.database_map = namespace.database_map
        return tenant_ctx

    def get_database_info(self, database_name: str) -> Optional[DatabaseInfo]:
        database: Optional[dict] = self.database_map.get(database_name, None)
        print(f"database:{database}")
        if database is None:
            return None
        else:
            return DatabaseInfo(
                db_url=database.get("db_url"),
                database_name=database.get("database_name"),
                user=database.get("user"),
                password=database.get("password"),
            )
