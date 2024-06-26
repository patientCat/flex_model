from app.domain.project_ctx.adaptor.repo import RepoService
from app.domain.project_ctx.adaptor.repo_factory import RepoFactory
from app.service.context import ContextHolder, ContextHolderImpl
from app.common import utils
from app.common.bizlogger import LOGGER
from app.common.error import BizException, ErrorCode
from app.domain.project_ctx.database import MongoDbContext
from app.domain.lowcode_model.dsl.dml_domain import DmlDomainFactory
from app.domain.lowcode_model.model_ctx.model import ModelNameContext, ModelContext, MetadataContext
from app.common.param.runtime import UpdateOneRequest, UpdateOneResponse, UpdateManyResponse, UpdateManyRequest, \
    FindOneRequest, FindOneResponse, FindManyRequest, FindManyResponse, CreateOneRequest, CreateOneResponse, \
    CreateManyResponse, CreateManyRequest, DeleteOneRequest, DeleteOneResponse, DeleteManyRequest, DeleteManyResponse
from app.repo import instance
from app.repo.interface import ModelRepo, DatabaseInstanceRepo


class RuntimeService:
    def __init__(self, context: ContextHolder, db_instance_repo: DatabaseInstanceRepo, model_repo: ModelRepo):
        self.context = context
        self.db_instance_repo: DatabaseInstanceRepo = db_instance_repo
        self.model_context_repo: ModelRepo = model_repo

    @staticmethod
    def create() -> "RuntimeService":
        instance.init()
        context = ContextHolderImpl(instance.db_instance_repo, instance.MODEL_REPO)
        return RuntimeService(context, instance.db_instance_repo, instance.MODEL_REPO)

    def _get_model_context(self, project_id: str, model_name: str) -> ModelContext:
        model_name_ctx = ModelNameContext(name=model_name, project_id=project_id)
        LOGGER.info("model_name_ctx=%s", utils.toJSON(model_name_ctx))

        model_context = self.context.get_model_context(project_id, model_name_ctx)
        if model_context is None:
            raise BizException(ErrorCode.InvalidParameter, f"name={model_name_ctx.name}_model_context is None")
        LOGGER.info("model_context=%s", model_context)
        return model_context

    def _get_database_context(self, model_context: ModelContext, project_id):
        model_name_ctx = model_context.model_name_ctx
        LOGGER.info("get_database_ctx, model_name_ctx=%s", utils.toJSON(model_name_ctx))
        database_info = self.context.get_database_info(project_id, model_context)
        if database_info is None:
            LOGGER.error(f"get_database_info_fail_with_project_id={project_id}")
            raise BizException(ErrorCode.InvalidParameter, "project_id relate database_info is not exist")
        LOGGER.info("get_database_ctx, database_info=%s", database_info.to_json())
        db_context = MongoDbContext(database_info, model_name_ctx.collection_name)
        return db_context

    def find_one(self, req: FindOneRequest) -> FindOneResponse:
        model_context = self._get_model_context(req.project_id, req.model_name)
        db_instance = self.db_instance_repo.get_db_instance_by_project_id(req.project_id)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, req.project_id)

        # 4. 获取Factory
        repo: RepoService = RepoFactory.create_repo(db_instance.db_type, db_context)
        find_domain = DmlDomainFactory(model_context).find_domain(param=req.param)
        record, total = repo.apply_find(find_domain)
        LOGGER.info("record={}".format(record))
        resp = FindOneResponse(record=record, total=total)
        return resp

    def find_many(self, req: FindManyRequest) -> FindManyResponse:
        model_context = self._get_model_context(req.project_id, req.model_name)
        db_instance = self.db_instance_repo.get_db_instance_by_project_id(req.project_id)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, req.project_id)

        # 4. 获取Factory
        repo: RepoService = RepoFactory.create_repo(db_instance.db_type, db_context)
        find_many_domain = DmlDomainFactory(model_context).find_many_domain(param=req.param)
        record, total = repo.apply_find_many(find_many_domain)
        LOGGER.info("record_list={}, total={}".format(record, total))
        resp = FindManyResponse(record=record, total=total)
        return resp

    def create_one(self, req: CreateOneRequest) -> CreateOneResponse:
        model_context: ModelContext = self._get_model_context(req.project_id, req.model_name)
        db_instance = self.db_instance_repo.get_db_instance_by_project_id(req.project_id)
        metadata_ctx: MetadataContext = model_context.get_master_metadata_ctx()
        if metadata_ctx is None:
            raise BizException(
                code=ErrorCode.InvalidParameter,
                message=f"metadata_ctx not exist, model_name={req.model_name}, project_id={req.project_id}"
            )
        domain = DmlDomainFactory(model_context).create_domain(
            param=req.param,
            metadata_ctx=metadata_ctx
        )

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, req.project_id)

        # 4. 获取Factory
        repo: RepoService = RepoFactory.create_repo(db_instance.db_type, db_context)
        insert_id = repo.apply_create(domain)
        resp = CreateOneResponse(id=insert_id)
        return resp

    def create_many(self, req: CreateManyRequest) -> CreateManyResponse:
        model_context = self._get_model_context(req.project_id, req.model_name)
        db_instance = self.db_instance_repo.get_db_instance_by_project_id(req.project_id)
        metadata_ctx: MetadataContext = model_context.get_master_metadata_ctx()
        if metadata_ctx is None:
            raise BizException(
                code=ErrorCode.InvalidParameter,
                message=f"metadata_ctx not exist, model_name={req.model_name}, project_id={req.project_id}"
            )
        create_many_domain = DmlDomainFactory(model_context).create_many_domain(
            param=req.param, metadata_ctx=metadata_ctx
        )
        # 3. 获取database_info
        db_context = self._get_database_context(model_context, req.project_id)

        # 4. 获取Factory
        repo: RepoService = RepoFactory.create_repo(db_instance.db_type, db_context)
        insert_id_list = repo.apply_create_many(create_many_domain)
        resp = CreateManyResponse(id_list=insert_id_list)
        return resp

    def update_one(self, req: UpdateOneRequest) -> UpdateOneResponse:
        model_context = self._get_model_context(req.project_id, req.model_name)
        db_instance = self.db_instance_repo.get_db_instance_by_project_id(req.project_id)
        metadata_ctx: MetadataContext = model_context.get_master_metadata_ctx()
        metadata_ctx.validate_on_update(req.param)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, req.project_id)

        # 4. 获取Factory
        domain = DmlDomainFactory(model_context).update_domain(param=req.param)
        repo: RepoService = RepoFactory.create_repo(db_instance.db_type, db_context)
        count = repo.apply_update(domain)
        resp = UpdateOneResponse(count=count)
        return resp

    def update_many(self, req: UpdateManyRequest) -> UpdateManyResponse:
        model_context = self._get_model_context(req.project_id, req.model_name)
        db_instance = self.db_instance_repo.get_db_instance_by_project_id(req.project_id)
        metadata_ctx: MetadataContext = model_context.get_master_metadata_ctx()
        metadata_ctx.validate_on_update(req.param)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, req.project_id)

        # 4. 获取Factory
        domain = DmlDomainFactory(model_context).update_many_domain(param=req.param)
        repo: RepoService = RepoFactory.create_repo(db_instance.db_type, db_context)
        count = repo.apply_update_many(domain)
        resp = UpdateManyResponse(count=count)
        return resp

    def delete_one(self, req: DeleteOneRequest) -> DeleteOneResponse:
        model_context = self._get_model_context(req.project_id, req.model_name)
        db_instance = self.db_instance_repo.get_db_instance_by_project_id(req.project_id)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, req.project_id)

        # 4. 获取Factory
        domain = DmlDomainFactory(model_context).delete_domain(param=req.param)
        repo: RepoService = RepoFactory.create_repo(db_instance.db_type, db_context)
        count = repo.apply_delete(domain)
        resp = DeleteOneResponse(count=count)
        return resp

    def delete_many(self, req: DeleteManyRequest) -> DeleteManyResponse:
        model_context = self._get_model_context(req.project_id, req.model_name)
        db_instance = self.db_instance_repo.get_db_instance_by_project_id(req.project_id)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, req.project_id)

        # 4. 获取Factory
        domain = DmlDomainFactory(model_context).delete_many_domain(param=req.param)
        repo: RepoService = RepoFactory.create_repo(db_instance.db_type, db_context)
        count = repo.apply_delete_many(domain)
        resp = DeleteManyResponse(count=count)
        return resp


RUNTIME_SERVICE = RuntimeService.create()
