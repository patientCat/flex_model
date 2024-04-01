from app.common import utils


class DatabaseInfo:
    def __init__(self, id: str = "", host: str = "", port: int = "27017", database_name: str = "", user: str = "",
                 password: str = ""):
        self.id = id
        self.host = host
        self.port = port
        self.database_name = database_name
        self.user = user
        self.password = password

    def get_db_url(self):
        pass

    def get_db_name(self):
        return self.database_name


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

    def database_info(self, database_name: str) -> DatabaseInfo:
        database = self.database_map.get(database_name, None)
        print(f"database:{database}")
        if database is None:
            return None
        else:
            return DatabaseInfo("id", **database)
