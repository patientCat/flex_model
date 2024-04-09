import json

from flask import Flask
from loguru import logger

from app.api.context import ContextHolder
from app.common import utils
from app.common.error import BizException, ErrorCode
from app.model.param.create import CreateOneRequest, CreateOneResponse, CreateManyRequest, CreateManyResponse
from app.model.param.find import FindOneRequest, FindOneResponse, FindManyRequest, FindManyResponse
from app.service.db_luster.context import MongoDbContext
from app.service.db_luster.mongo import reposervice
from app.service.model_domain.dsl.create_domain import CreateDomainFactory
from app.service.model_domain.dsl.find_domain import FindDomainFactory
from app.service.model_domain.metadata.model import ModelNameCtx


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

    def findOne(self, req: FindOneRequest) -> FindOneResponse:
        model_context, model_name_ctx = self._get_model_context(req.tenant_id, req.model_name)

        # 3. 获取database_info
        dbcontext = self._get_database_context(model_context, model_name_ctx, req)

        # 4. 获取Factory
        find_domain = FindDomainFactory(model_context).create_domain(req.param)
        create_repo = reposervice.FindRepoService(dbcontext, find_domain)
        record = create_repo.apply()
        logger.info("record={}".format(record))
        resp = FindOneResponse(record=record)
        return resp

    def findMany(self, req: FindManyRequest) -> FindManyResponse:
        model_context, model_name_ctx = self._get_model_context(req.tenant_id, req.model_name)

        # 3. 获取database_info
        dbcontext = self._get_database_context(model_context, model_name_ctx, req)

        # 4. 获取Factory
        find_domain = FindDomainFactory(model_context).create_domain(req.param)
        create_repo = reposervice.FindRepoService(dbcontext, find_domain)
        record = create_repo.apply()
        logger.info("record={}".format(record))
        resp = FindManyResponse(record={"x": 1}, total=5)
        return resp

    def createOne(self, req: CreateOneRequest) -> CreateOneResponse:
        # 1. TODO validate by schema
        model_context, model_name_ctx = self._get_model_context(req.tenant_id, req.model_name)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, model_name_ctx, req)

        # 4. 获取Factory
        create_domain = CreateDomainFactory(model_context).create_domain(req.param)
        create_repo = reposervice.CreateRepoService(db_context, create_domain)
        insert_id = create_repo.apply(create_domain)
        resp = CreateOneResponse(id=insert_id)
        return resp

    def createMany(self, req: CreateManyRequest) -> CreateManyResponse:
        # 1. TODO validate by schema
        model_context, model_name_ctx = self._get_model_context(req.tenant_id, req.model_name)

        # 3. 获取database_info
        db_context = self._get_database_context(model_context, model_name_ctx, req)

        # 4. 获取Factory
        create_many_domain = CreateDomainFactory(model_context).create_many_domain(req.param)
        create_repo = reposervice.CreateRepoService(db_context)
        insert_id_list = create_repo.apply_many(create_many_domain)
        resp = CreateManyResponse(id_list=insert_id_list)
        return resp
