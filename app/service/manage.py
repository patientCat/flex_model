from typing import List

import sqlalchemy

from app.common.error import BizException, ErrorCode
from app.common.model_converter import ModelConverter
from app.common.param.manage import CreateModelRequest, CreateModelResponse, GetModelRequest, GetModelListRequest, \
    GetModelResponse, GetModelListResponse, DeleteModelRequest, DeleteModelResponse, AddColumnRequest, \
    ModifyColumnRequest, DeleteColumnRequest, AddColumnResponse, ModifyColumnResponse, DeleteColumnResponse, \
    CreateDatabaseInstanceRequest, CreateDatabaseInstanceResponse, GetDatabaseInstanceRequest, \
    GetDatabaseInstanceResponse, DatabaseInstanceVo, DeleteDatabaseInstanceRequest, DeleteDatabaseInstanceResponse
from app.domain.lowcode_model.model_ctx.model import ModelContext, ModelNameContext
from app.repo.instance import MODEL_REPO, db_instance_repo
from app.repo.po import DatabaseInstancePO, ModelPO


class ManageService:
    def __init__(self):
        self.model_repo = MODEL_REPO
        self.db_instance_repo = db_instance_repo

    @staticmethod
    def create():
        return ManageService()

    def create_model(self, req: CreateModelRequest) -> CreateModelResponse:
        db_instance: DatabaseInstancePO = self.db_instance_repo.get_db_instance_by_project_id(project_id=req.project_id)
        if db_instance is None:
            raise BizException(code=ErrorCode.InvalidParameter,
                               message=f"Project with id {req.project_id} is not found")

        model_name_ctx = ModelNameContext.validate_and_create(name=req.model_name, project_id=req.project_id)
        model_context = ModelContext.create(model_name_ctx=model_name_ctx, model_repo=self.model_repo)
        model_context.create_metadata_ctx(schema=req.schema, db_type=db_instance.db_type)
        return CreateModelResponse(success=True)

    def get_model(self, req: GetModelRequest) -> GetModelResponse:
        model_po = self.__get_model(project_id=req.project_id, model_name=req.model_name)

        return GetModelResponse(model=ModelConverter.convert_model_po_2_vo(model_po))

    def get_model_list(self, req: GetModelListRequest) -> GetModelListResponse:
        model_po_list: List[ModelPO] = self.model_repo.get_model_list_page(project_id=req.project_id,
                                                                           page_size=req.page_size,
                                                                           page_num=req.page_number)
        if model_po_list is None:
            model_po_list = []

        return GetModelListResponse(model_list=ModelConverter.convert_model_list_po_2_vo(model_po_list))

    def delete_model(self, req: DeleteModelRequest) -> DeleteModelResponse:
        self.model_repo.delete_model_by_name(project_id=req.project_id, model_name=req.model_name)
        return DeleteModelResponse(success=True)

    def add_column(self, req: AddColumnRequest) -> AddColumnResponse:
        model_name_ctx = ModelNameContext.validate_and_create(name=req.model_name, project_id=req.project_id)
        model_context = ModelContext.create(model_name_ctx=model_name_ctx, model_repo=self.model_repo)

        model_context.add_column(req.column_list)

        return AddColumnResponse(True)

    def modify_column(self, req: ModifyColumnRequest) -> ModifyColumnResponse:
        model_po = self.__get_model(project_id=req.project_id, model_name=req.model_name)
        return ModifyColumnResponse(success=True)

    def __get_model(self, *, project_id, model_name) -> ModelPO:
        model_po: ModelPO = self.model_repo.get_model_by_name(project_id=project_id, model_name=model_name)
        if model_po is None:
            raise BizException(code=ErrorCode.InvalidParameter,
                               message=f"Model with name '{model_name}' is not found")
        return model_po

    def delete_column(self, req: DeleteColumnRequest) -> DeleteColumnResponse:
        model_name_ctx = ModelNameContext.validate_and_create(name=req.model_name, project_id=req.project_id)
        model_context = ModelContext.create(model_name_ctx=model_name_ctx, model_repo=self.model_repo)

        model_context.delete_column(req.column_name_list)
        return DeleteColumnResponse(True)

    def create_database_instance(self, req: CreateDatabaseInstanceRequest) -> CreateDatabaseInstanceResponse:
        database_instance_po: DatabaseInstancePO = DatabaseInstancePO()
        database_instance_po.project_id = req.project_id
        database_instance_po.db_type = req.type
        database_instance_po.host = req.host
        database_instance_po.port = req.port
        database_instance_po.db_name = req.database_name
        database_instance_po.user_name = req.username
        database_instance_po.password = req.password

        try:
            self.db_instance_repo.create_db_instance(database_instance_po)
        except Exception as e:
            if isinstance(e, sqlalchemy.exc.IntegrityError):
                raise BizException(ErrorCode.InvalidParameter,
                                   f"project='{req.project_id}' already exists")
            raise e
        return CreateDatabaseInstanceResponse(success=True)

    def get_database_instance(self, req: GetDatabaseInstanceRequest) -> GetDatabaseInstanceResponse:

        db_instance_po: DatabaseInstancePO = self.db_instance_repo.get_db_instance_by_project_id(req.project_id)
        db_instance_vo = DatabaseInstanceVo(project_id=db_instance_po.project_id,
                                            db_type=db_instance_po.db_type,
                                            host=db_instance_po.host,
                                            db_name=db_instance_po.db_name)
        return GetDatabaseInstanceResponse(db_instance_vo)

    def delete_database_instance(self, req: DeleteDatabaseInstanceRequest) -> DeleteDatabaseInstanceResponse:
        self.db_instance_repo.remove_by_project_id(project_id=req.project_id)
        return DeleteDatabaseInstanceResponse(success=True)


MANAGE_SERVICE: ManageService = ManageService()
