from dataclasses import dataclass

from app.common.error import BizException, ErrorCode


class BaseRequest:
    def __init__(self, **kwargs):
        self.model_name: str = kwargs.get('ModelName')
        if self.model_name is None:
            raise BizException(ErrorCode.InvalidParameter, 'ModelName is None')
        self.project_id: str = kwargs.get('ProjectId')
        if self.project_id is None:
            raise BizException(ErrorCode.InvalidParameter, 'ProjectId is None')
        self.param: dict = kwargs.get('Param')


class CreateOneRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class CreateOneResponse:
    id: str

    def dict_msg(self):
        return {
            "Id": self.id,
        }


class CreateManyRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class CreateManyResponse:
    id_list: list

    def dict_msg(self):
        return {
            "IdList": self.id_list
        }


class FindOneRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class FindOneResponse:
    record: dict
    total: int

    def dict_msg(self):
        return {
            "Record": self.record,
            "Total": self.total
        }


class FindManyRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class FindManyResponse:
    record: dict
    total: int

    def dict_msg(self):
        return {
            "Record": self.record,
            "Total": self.total
        }


class UpdateOneRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class UpdateOneResponse:
    count: int

    def dict_msg(self):
        return {
            "Count": self.count,
        }


class UpdateManyRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class UpdateManyResponse:
    count: int

    def dict_msg(self):
        return {
            "Count": self.count
        }

class DeleteOneRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class DeleteOneResponse:
    count: int

    def dict_msg(self):
        return {
            "Count": self.count,
        }


class DeleteManyRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class DeleteManyResponse:
    count: int

    def dict_msg(self):
        return {
            "Count": self.count
        }
