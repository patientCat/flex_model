from app.api.context import ContextHolder
from app.model.param.create import CreateOneRequest, CreateOneResponse
from app.model.param.find import FindOneRequest, FindOneResponse
from app.service.model_domain.dsl.create_domain import CreateDomainFactory
from app.service.model_domain.metadata.model import ModelName
from app.service.model_repo.context import MongoDbContext
from app.service.model_repo.mongo import reposervice


class RuntimeService:
    def __init__(self, context: ContextHolder):
        self.context = context

    def findOne(self, req: FindOneRequest) -> FindOneResponse:
        return "findOne"

    def createOne(self, req: CreateOneRequest) -> CreateOneResponse:
        # 1 validate by schema
        model_name = ModelName(req.model_name, req.model_namespace)
        model_context = self.context.get_model_context(model_name)

        create_domain = CreateDomainFactory(model_context).create_domain(req.param)
        database_info = self.context.get_database_info(req.tenant_id, model_context)
        dbcontext = MongoDbContext(database_info, model_name)
        create_repo = reposervice.CreateRepoService(dbcontext, create_domain)
        return create_repo.apply()
