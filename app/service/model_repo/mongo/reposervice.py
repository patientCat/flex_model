from app.service.model_domain.dsl.create_domain import CreateDomain
from app.service.model_repo import context


class CreateRepoService:
    def __init__(self, db_context: context.DbContext, create_domain : CreateDomain):
        self.db_context = db_context
        self.create_domain = create_domain

    """
    1. 连接数据库
    2. 执行插入操作
    """

    def apply(self):
        # 连接到MongoDB服务器
        client = self.db_context.create_client()

        # 选择一个数据库
        db = client[self.db_context.database_name]
        # 选择一个集合（类似于表）
        collection = db[self.db_context.table_name.collection_name()]
        result = collection.insert_one(self.create_domain.data)
        return result.inserted_id

