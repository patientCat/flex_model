from abc import abstractmethod

from loguru import logger

from app.common import utils
from app.common.error import BizException, ErrorCode
from app.domain.lowcode_model.model_ctx.model import ModelContext, ModelNameContext
from app.domain.tenant.tenant import TenantContext, DatabaseInfo


class ContextHolder:
    pass

    @abstractmethod
    def get_model_context(self, tenant_id: str, model_name: ModelNameContext) -> ModelContext:
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
            "name": {"type": "string", "x-format": "x-short-text"},
            "age": {"type": "number", "x-format": "x-number"},
            "relation": {"type": "number", "x-format": "x-many-to-one"}
        }
    }

    example_tenant = {
        "name": "tenant",
        "database_map": {
            "test_database": {
                "db_url": "mongodb://localhost:27017/",
                "database_name": "test_db",
                "user": "",
                "password": ""
            }
        }
    }

    def __init__(self):
        super().__init__()
        self.__model_context: ModelContext = ModelContext.create_from_schema(self.example_schema)
        self.__tenant_context: TenantContext = TenantContext.create_from_json(self.example_tenant)

    @abstractmethod
    def get_model_context(self, tenant_id, model_name: ModelNameContext) -> ModelContext:
        return self.__model_context

    @abstractmethod
    def get_database_info(self, tenant_id, model_ctx: ModelContext) -> DatabaseInfo:
        database_name = model_ctx.database_identity.database_name
        logger.info("tenant_context={}", utils.toJSON(self.__tenant_context))
        database_info = self.__tenant_context.get_database_info(database_name)
        if database_info is None:
            raise BizException(ErrorCode.InternalError,
                               f"database_name={database_name} not exist in tenant={self.__tenant_context.id}")
        return database_info
