import json

from flask import Flask
from loguru import logger

from app.api.context import ContextHolder
from app.common import utils
from app.common.error import BizException, ErrorCode
from app.model.param.create import CreateOneRequest, CreateOneResponse
from app.model.param.find import FindOneRequest, FindOneResponse
from app.service.db_luster.context import MongoDbContext
from app.service.db_luster.mongo import reposervice
from app.service.model_domain.dsl.create_domain import CreateDomainFactory
from app.service.model_domain.metadata.model import ModelNameCtx


class RuntimeService:
    def __init__(self, context: ContextHolder):
        self.context = context

    def findOne(self, req: FindOneRequest) -> FindOneResponse:
        resp = FindOneResponse(record={"x": 1}, total=5)
        return resp

    def createOne(self, req: CreateOneRequest) -> CreateOneResponse:
        # 1 validate by schema
        model_name_ctx = ModelNameCtx(req.model_name)
        logger.info("model_name_ctx={}", utils.toJSON(model_name_ctx))
        model_context = self.context.get_model_context(req.tenant_id, model_name_ctx)
        if model_context is None:
            raise BizException(ErrorCode.InvalidParameter, f"name={model_name_ctx.name}_model_context is None")
        logger.info("model_context={}", utils.toJSON(model_context))

        create_domain = CreateDomainFactory(model_context).create_domain(req.param)
        database_info = self.context.get_database_info(req.tenant_id, model_context)
        dbcontext = MongoDbContext(database_info, model_name_ctx)
        create_repo = reposervice.CreateRepoService(dbcontext, create_domain)
        insert_id = create_repo.apply()
        create_resp = CreateOneResponse(id=insert_id)
        return create_resp
