from app.domain.lowcode_model.dsl.dsl_domain import CreateTableDomain
from app.domain.project_ctx.adaptor.repo import RepoService


class MysqlRepoService(RepoService):
    def __init__(self):
        pass

    def create_table(self, domain: CreateTableDomain):
        pass
