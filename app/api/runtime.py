import json

from flask import Flask
from loguru import logger

from app.api.context import ContextHolder
from app.common import utils
from app.common.error import BizException, ErrorCode
from app.domain.database_ctx.context import MongoDbContext
from app.domain.database_ctx.mongo import reposervice
from app.domain.lowcode_model.dsl.dsl_domain import DomainFactory
from app.domain.lowcode_model.model_ctx.model import ModelNameCtx
from app.model.param.runtime import UpdateOneRequest, UpdateOneResponse, UpdateManyResponse, UpdateManyRequest, \
    FindOneRequest, FindOneResponse, FindManyRequest, FindManyResponse, CreateOneRequest, CreateOneResponse, \
    CreateManyResponse, CreateManyRequest, DeleteOneRequest, DeleteOneResponse, DeleteManyRequest, DeleteManyResponse


class RuntimeService:
    def __init__(self, context: ContextHolder):
        self.context = context

    def _get_model_context(self, tenant_id: str, model_name: str):
        model_name_ctx = ModelNameCtx(model_name)
        logger.info("model_name_ctx={}", utils.toJSON(model_name_ctx))

        model_context = self.context.get_model_context(tenant_id, model_name_ctx)
        if model_context is None:
            raise BizException(ErrorCode.InvalidParameter, f"name={model_name_ctx.name}_model_context is None")
        logger.info("model_context={}", utils.toJSON(model_context))
        return model_context, model_name_ctx

    def _get_database_context(self, model_context, model_name_ctx, req):
        database_info = self.context.get_database_info(req.tenant_id, model_context)
        dbcontext = MongoDbContext(database_info, model_name_ctx.collection_name)
        return dbcontext

    def find_one(self, req: FindOneRequest) -> FindOneResponse:
        model_context, model_name_ctx = self._get_model_context(req.tenant_id, req.model_name)

        # 3. 获取database_info
        dbcontext = self._get_database_context(model_context, model_name_ctx, req)

        # 4. 获取Factory
        mongo_repo = reposervice.MongoRepoService(dbcontext)
        find_domain = DomainFactory(model_context).find_domain(req.param)
        record, total = mongo_repo.apply_find(find_domain)
        logger.info("record={}".format(record))
        resp = FindOneResponse(record=record, total=total)
        return resp

    def find_many(self, req: FindManyRequest) -> FindManyResponse:
        model_context, model_name_ctx = self._get_model_context(req.tenant_id, req.model_name)

        # 3. 获取database_info
        dbcontext = self._get_database_context(model_context, model_name_ctx, req)

        # 4. 获取Factory
        mongo_repo = reposervice.MongoRepoService(dbcontext)
        find_many_domain = DomainFactory(model_context).find_many_domain(req.param)
        record, total = mongo_repo.apply_find_many(find_many_domain)
        logger.info("record_list={}, total={}".format(record, total))
        resp = FindManyResponse(record=record, total=total)
        return resp

    def create_one(self, req: CreateOneRequest) -> CreateOneResponse:
        # 1. TODO validate by schema
        model_context, model_name_ctx = self._get_model_context(req.tenant_id, req.model_name)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, model_name_ctx, req)

        # 4. 获取Factory
        domain = DomainFactory(model_context).domain(req.param)
        mongo_repo = reposervice.MongoRepoService(db_context)
        insert_id = mongo_repo.apply_create(domain)
        resp = CreateOneResponse(id=insert_id)
        return resp

    def create_many(self, req: CreateManyRequest) -> CreateManyResponse:
        # 1. TODO validate by schema
        model_context, model_name_ctx = self._get_model_context(req.tenant_id, req.model_name)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, model_name_ctx, req)

        # 4. 获取Factory
        create_many_domain = DomainFactory(model_context).create_many_domain(req.param)
        mongo_repo = reposervice.MongoRepoService(db_context)
        insert_id_list = mongo_repo.apply_many(create_many_domain)
        resp = CreateManyResponse(id_list=insert_id_list)
        return resp

    def update_one(self, req: UpdateOneRequest) -> UpdateOneResponse:
        # 1. TODO validate by schema
        model_context, model_name_ctx = self._get_model_context(req.tenant_id, req.model_name)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, model_name_ctx, req)

        # 4. 获取Factory
        domain = DomainFactory(model_context).update_domain(req.param)
        mongo_repo = reposervice.MongoRepoService(db_context)
        count = mongo_repo.apply_update(domain)
        resp = UpdateOneResponse(count=count)
        return resp

    def update_many(self, req: UpdateManyRequest) -> UpdateManyResponse:
        # 1. TODO validate by schema
        model_context, model_name_ctx = self._get_model_context(req.tenant_id, req.model_name)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, model_name_ctx, req)

        # 4. 获取Factory
        domain = DomainFactory(model_context).update_many_domain(req.param)
        mongo_repo = reposervice.MongoRepoService(db_context)
        count = mongo_repo.apply_update_many(domain)
        resp = UpdateManyResponse(count=count)
        return resp

    def delete_one(self, req: DeleteOneRequest) -> DeleteOneResponse:
        model_context, model_name_ctx = self._get_model_context(req.tenant_id, req.model_name)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, model_name_ctx, req)

        # 4. 获取Factory
        domain = DomainFactory(model_context).delete_domain(req.param)
        mongo_repo = reposervice.MongoRepoService(db_context)
        count = mongo_repo.apply_delete(domain)
        resp = DeleteOneResponse(count=count)
        return resp

    def delete_many(self, req: DeleteManyRequest) -> DeleteManyResponse:
        model_context, model_name_ctx = self._get_model_context(req.tenant_id, req.model_name)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, model_name_ctx, req)

        # 4. 获取Factory
        domain = DomainFactory(model_context).delete_many_domain(req.param)
        mongo_repo = reposervice.MongoRepoService(db_context)
        count = mongo_repo.apply_delete_many(domain)
        resp = DeleteManyResponse(count=count)
        return resp
