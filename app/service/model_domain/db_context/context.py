class Table:
    def __init__(self, table_name: str, use_ns=True, ns: str = "default"):
        self.use_ns = use_ns
        self.namespace = ns
        self.table_name = table_name

    def collection_name(self) -> str:
        if self.use_ns:
            return f"{self.namespace}_{self.table_name}"
        else:
            return self.table_name


class DbContext:
    def __init__(self, db_url, database_name: str, table: Table):
        self.db_url = db_url
        self.database_name = database_name
        self.table = table
