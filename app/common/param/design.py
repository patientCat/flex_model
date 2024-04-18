import json
from dataclasses import dataclass
from typing import List

from app.common.error import BizException, ErrorCode


class BaseDesignRequest:
    def __init__(self, **kwargs):
        self.project_id: str = kwargs.get('ProjectId')
        if self.project_id is None:
            raise BizException(ErrorCode.InvalidParameter, 'ProjectId is None')


class CreateModelRequest(BaseDesignRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.description: str = kwargs.get('Description')
        self.model_name: str = kwargs.get('ModelName')
        self.schema: dict = kwargs.get('ModelSchema')


@dataclass
class CreateModelResponse:
    success: bool

    def dict_msg(self):
        return {
            "Success": self.success,
        }


class GetModelRequest(BaseDesignRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name: str = kwargs.get('ModelName')
        self.schema: dict = kwargs.get('ModelSchema')


@dataclass
class ModelVO:
    name: str
    schema: str

    def dict_msg(self):
        return {
            "Name": self.name,
            "Schema": self.schema
        }


@dataclass
class GetModelResponse:
    model: ModelVO

    def dict_msg(self):
        return {
            "Model": self.model.dict_msg(),
        }


class GetModelListRequest(BaseDesignRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page_size: int = kwargs.get('PageSize')
        self.page_number: int = kwargs.get('PageNumber')


@dataclass
class GetModelListResponse:
    model_list: List[ModelVO]

    def dict_msg(self):
        return {
            "ModelList": [x.dict_msg() for x in self.model_list],
        }


class DeleteModelRequest(BaseDesignRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name: int = kwargs.get('ModelName')


@dataclass
class DeleteModelResponse:
    success: bool

    def dict_msg(self):
        return {
            "Success": self.success
        }
