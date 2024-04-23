from typing import List

from app.common.error import BizException, ErrorCode
from app.common.model_converter import ModelConverter
from app.common.param.design import CreateModelRequest, CreateModelResponse, GetModelRequest, GetModelListRequest, \
    GetModelResponse, GetModelListResponse, DeleteModelRequest, DeleteModelResponse
from app.domain.lowcode_model.model_ctx.model import ModelContext, ModelNameContext
from app.repo.instance import MODEL_REPO, PROJECT_REPO
from app.repo.po import ProjectPO, ModelPO


class DesignService:
    def __init__(self):
        self.model_repo = MODEL_REPO
        self.project_repo = PROJECT_REPO

    @staticmethod
    def create():
        return DesignService()

    def create_model(self, req: CreateModelRequest) -> CreateModelResponse:
        project: ProjectPO = self.project_repo.get_project_by_project_id(project_id=req.project_id)
        if project is None:
            raise BizException(code=ErrorCode.InvalidParameter, message=f"Project with id {req.project_id} is not found")

        model_name_ctx = ModelNameContext.validate_and_create(name=req.model_name, project_id=req.project_id)
        model_context = ModelContext.create(model_name_ctx=model_name_ctx, model_repo=self.model_repo)
        model_context.create_metadata_ctx(schema=req.schema)
        return CreateModelResponse(success=True)

    def get_model(self, req: GetModelRequest) -> GetModelResponse:
        model_po: ModelPO = self.model_repo.get_model_by_name(project_id=req.project_id, model_name=req.model_name)
        if model_po is None:
            raise BizException(code=ErrorCode.InvalidParameter,
                               message=f"Model with name '{req.model_name}' is not found")

        return GetModelResponse(model=ModelConverter.convert_model_po_2_vo(model_po))

    def get_model_list(self, req: GetModelListRequest) -> GetModelListResponse:
        model_po_list: List[ModelPO] = self.model_repo.get_model_list_page(project_id=req.project_id,
                                                                           page_size=req.page_size,
                                                                           page_num=req.page_number)
        if model_po_list is None:
            model_po_list = []

        return GetModelListResponse(model_list=ModelConverter.convert_model_list_po_2_vo(model_po_list))

    def delete_model(self, req: DeleteModelRequest) -> DeleteModelResponse:
        self.model_repo.delete_model(project_id=req.project_id, model_name=req.model_name)
        return DeleteModelResponse(success=True)


DESIGN_SERVICE = DesignService()
