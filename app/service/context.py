from abc import abstractmethod

from app.domain.lowcode_model.model_ctx.model import ModelContext, ModelNameContext
from app.domain.project_ctx.project import ProjectContext, DatabaseInfo
from app.repo.interface import ModelRepo, DatabaseInstanceRepo


class ContextHolder:

    @abstractmethod
    def get_model_context(self, project_id: str, model_name: ModelNameContext) -> ModelContext:
        pass

    # 通过模型上下文，拿到数据库上下文
    @abstractmethod
    def get_database_info(self, project_id: str, model_ctx: ModelContext) -> DatabaseInfo:
        pass


class ContextHolderImpl(ContextHolder):
    def __init__(self, db_instance_repo: DatabaseInstanceRepo, model_repo: ModelRepo):
        self.db_instance_repo = db_instance_repo
        self.model_repo = model_repo

    # 通过模型标识获取model_context
    @abstractmethod
    def get_model_context(self, project_id: str, model_name: ModelNameContext) -> ModelContext:
        return ModelContext.create(model_name_ctx=model_name, model_repo=self.model_repo)

    # 通过模型上下文，拿到数据库上下文
    @abstractmethod
    def get_database_info(self, project_id: str, model_ctx: ModelContext) -> DatabaseInfo:
        return ProjectContext(db_instance_repo=self.db_instance_repo).get_database_info(project_id=project_id)
