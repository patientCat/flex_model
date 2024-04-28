from dataclasses import dataclass
from typing import List

from app.common.error import BizException, ErrorCode


class BaseProjectRequest:
    def __init__(self, **kwargs):
        self.project_id: str = kwargs.get('ProjectId')
        if self.project_id is None:
            raise BizException(ErrorCode.InvalidParameter, 'ProjectId is None')


class CreateModelRequest(BaseProjectRequest):
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


class GetModelRequest(BaseProjectRequest):
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


class GetModelListRequest(BaseProjectRequest):
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


class DeleteModelRequest(BaseProjectRequest):
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


class AddColumnRequest(BaseProjectRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name: str = kwargs.get('ModelName')
        self.column_list: List[dict] = kwargs.get('ColumnList')


@dataclass
class AddColumnResponse:
    success: bool

    def dict_msg(self):
        return {
            "Success": self.success
        }


class DeleteColumnRequest(BaseProjectRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name: str = kwargs.get('ModelName')
        self.column_name_list: List[str] = kwargs.get('ColumnNameList')


@dataclass
class DeleteColumnResponse:
    success: bool

    def dict_msg(self):
        return {
            "Success": self.success
        }


class ModifyColumnRequest(BaseProjectRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name: str = kwargs.get('ModelName')
        self.column_name_list: List[str] = kwargs.get('ColumnNameList')


@dataclass
class ModifyColumnResponse:
    success: bool

    def dict_msg(self):
        return {
            "Success": self.success
        }


class CreateDatabaseInstanceRequest(BaseProjectRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type: str = kwargs.get('Type')
        self.database_url: str = kwargs.get('DatabaseUrl')
        self.database_name: str = kwargs.get('DatabaseName')


@dataclass
class CreateDatabaseInstanceResponse:
    success: bool

    def dict_msg(self):
        return {
            "Success": self.success
        }


class GetDatabaseInstanceRequest(BaseProjectRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

@dataclass
class DatabaseInstanceVo:
    project_id: str
    db_type: str
    db_url: str
    db_name: str

    def dict_msg(self):
        return {
            "ProjectId": self.project_id,
            "Type": self.db_type,
            "DatabaseUrl": self.db_url,
            "DatabaseName": self.db_name,
        }

@dataclass
class GetDatabaseInstanceResponse:
    db_instance: DatabaseInstanceVo

    def dict_msg(self):
        return {
            "Instance": self.db_instance.dict_msg()
        }

