from typing import List, Optional

from app.common.error import ErrorCode, BizException
from app.service.model_domain.metadata.model import ModelContext


class CreateDomain:
    def __init__(self, data: dict):
        self.data = data


class CreateManyDomain:
    def __init__(self, datalist: List[dict]):
        self.datalist = datalist


class CreateDomainFactory:
    KEY_DATA = "data"
    KEY_DATALIST = "datalist"

    ERROR_KEY_DATA_NOT_FOUND = "key `data` not found, reference : {'data':{'foo':'bar'}}"
    ERROR_INVALID_DATA_VALUE = "value `data` should be dict, reference : {'data':{'foo':'bar'}}"
    ERROR_KEY_DATALIST_NOT_FOUND = "key `datalist` not found, reference : {'datalist':[{'foo':'bar'}]}"
    ERROR_INVALID_DATALIST_VALUE = "value `datalist` should be List[dict], reference : {'datalist':[{'foo':'bar'}]}"
    ERROR_PARAM_IS_NONE = "param can not be none"

    def __init__(self, model_context: ModelContext):
        self.model_context = model_context

    def create_domain(self, dict_param: Optional[dict]) -> CreateDomain:
        if dict_param is None:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        if self.KEY_DATA not in dict_param:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_KEY_DATA_NOT_FOUND)
        data_ = dict_param[self.KEY_DATA]
        if not isinstance(data_, dict):
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        ## todo filter key by model_context
        return CreateDomain(data_)

    def create_many_domain(self, dict_param: Optional[dict]) -> CreateManyDomain:
        if dict_param is None:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        if self.KEY_DATALIST not in dict_param:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_KEY_DATALIST_NOT_FOUND)
        datalist_ = dict_param[self.KEY_DATALIST]
        if not isinstance(datalist_, list):
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_INVALID_DATALIST_VALUE)
        ## todo filter key by model_context
        return CreateManyDomain(datalist_)
