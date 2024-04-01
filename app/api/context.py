from abc import abstractmethod

from app.common.error import BizException, ErrorCode
from app.service.model_domain.metadata.model import ModelContext, ModelName
from app.service.tenant.tenant import TenantContext, DatabaseInfo


class ContextHolder:
    pass

    @abstractmethod
    def get_model_context(self, model_name: ModelName) -> ModelContext:
        pass

    # 通过模型上下文，拿到数据库上下文
    @abstractmethod
    def get_database_info(self, tenant_id: str, model_ctx: ModelContext) -> DatabaseInfo:
        pass


class TestContextHolder(ContextHolder):
    example_schema = {
        "x-model-name": "test_model",
        "x-database-name": "test_database",
        "type": "object",
        "properties": {
            "id": {"type": "integer", "x-format": "x-short-text"},
            "name": {"type": "number", "x-format": "x-number"},
            "relation": {"type": "number", "x-format": "x-many-to-one"}
        }
    }

    example_tenant = {
        "name": "tenant",
        "database_map": {
            "test_database": {
                "host": "localhost",
                "port": 27017,
                "database_name": "test_database",
                "user": "",
                "password": ""
            }
        }
    }

    def __init__(self):
        super().__init__()
        self.model_context_ = ModelContext.create_from_schema(self.example_schema)
        self.tenant_context = TenantContext.create_from_json(self.example_tenant)

    @abstractmethod
    def get_model_context(self, model_name: ModelName) -> ModelContext:
        return self.model_context_

    @abstractmethod
    def get_database_info(self, tenant_id, model_ctx: ModelContext) -> DatabaseInfo:
        database_name = model_ctx.database_identity.database_name
        db_context_ = self.tenant_context.get_database_info(tenant_id, database_name)
        if db_context_ is None:
            raise BizException(ErrorCode.InternalError,
                               f"database_name={database_name} not exist in tenant={self.tenant_context.id}")
        return db_context_
