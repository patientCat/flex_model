from app.domain.project_ctx.adaptor.mongo_repo import MongoRepoService
from app.domain.project_ctx.adaptor.mysql_repo import MysqlRepoService
from app.domain.project_ctx.adaptor.repo import RepoService
from app.domain.project_ctx.database import DbContext


class RepoFactory:
    @staticmethod
    def create_repo(db_type: str, db_context: DbContext) -> RepoService:
        if db_type == "mongo":
            return MongoRepoService(db_context)
        elif db_type == "mysql":
            return MysqlRepoService()
        else:
            raise RuntimeError(f"Unknown repo type {db_type}")
