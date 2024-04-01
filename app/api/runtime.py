from app.api.context import ContextHolder
from app.model.param.create import CreateOneRequest, CreateOneResponse
from app.model.param.find import FindOneRequest, FindOneResponse
from app.service.model_domain.dsl.create_domain import CreateDomainFactory
from app.service.model_repo.context import MongoDbContext
from app.service.model_repo.mongo import reposervice


class RuntimeService:
    def __init__(self, context: ContextHolder):
        self.context = context
        self.create_domain_factory = CreateDomainFactory(context.model_context())

    def findOne(self, req: FindOneRequest) -> FindOneResponse:
        return "findOne"

    def createOne(self, req: CreateOneRequest) -> CreateOneResponse:
        # 1 validate by schema
        create_domain = CreateDomainFactory.create_domain(req.param)
        database_info = self.context.database_info(self.context.model_context())
        dbcontext = MongoDbContext(database_info.get_db_url(), database_info.get_db_name())
        create_repo = reposervice.CreateRepoService(dbcontext, create_domain)
        return create_repo.apply()
