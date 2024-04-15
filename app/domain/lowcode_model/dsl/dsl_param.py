from dataclasses import dataclass
from typing import Dict, Union, Optional, List

from app.common.error import BizException, ErrorCode
from app.domain.lowcode_model.model_ctx import model, field
from app.domain.lowcode_model.model_ctx.model import MetadataContext

"""
dsl option

selector

pagination


"""


class Selector:
    def __init__(self, select_dict: dict):
        self.select_dict = select_dict

    def __repr__(self):
        return f"{self.__class__.__name__}(select_dict= {self.select_dict.__repr__()})"


class SelectorFactory:
    KEY_SELECT = 'select'

    """
    Args:
        1. model_contex (model.ModelContext) : the model class that will be selected
    """

    def __init__(self, model_contex: model.ModelContext):
        self.model_context: model.ModelContext = model_contex

    """
    Args:
        1. select_dict (Dict)             : a dict contains all fields and conditions

    Example:
        Selector(model_class=ExampleModelClass, select_dict={'select':{'a':1, 'b':1, 'c':0 'sub_table':{'sub_a':1, 'sub_b':1}}}
        1 stands for selecting this field
        0 stands for not selecting this field
    """

    def create_selector(self, select_dict: Dict[str, Union[int, Dict]]):
        new_dict = {}
        if self.KEY_SELECT not in select_dict:
            # select all
            new_dict = self.select_all()
        else:
            new_dict = self.select_target(select_dict[self.KEY_SELECT])
        return Selector(new_dict)

    def select_all(self) -> Dict[str, Union[int, Dict]]:
        new_select_dict: Dict[str, Union[int, Dict[str, 1]]] = {}
        master_metadata_ctx: MetadataContext = self.model_context.get_master_metadata_ctx()
        column_list: List[field.SchemaColumn] = master_metadata_ctx.column_list
        for column in column_list:
            if not column.is_relation():
                new_select_dict[column.key] = 1

        return new_select_dict

    def filter_non_zero(self, select_dict: Dict[str, Union[int, Dict]]) -> Dict[str, Union[int, Dict]]:
        new_dict = {}
        for k, v in select_dict.items():
            if isinstance(v, dict):
                sub_dict = self.filter_non_zero(v)
                if sub_dict:
                    new_dict[k] = sub_dict
            elif isinstance(v, int):
                if v > 0:
                    new_dict[k] = 1
            elif isinstance(v, bool):
                if v is True:
                    new_dict[k] = 1
        return new_dict

    def select_target(self, select_dict: Dict[str, Union[int, Dict]]) -> Dict[str, Union[int, Dict]]:
        # 从select_dict中过滤掉非0值
        new_select = self.filter_non_zero(select_dict)

        # 过滤掉非model_context中字段
        # todo
        return new_select


@dataclass
class Pagination:
    limit: int = 10
    offset: int = 0


class PaginationFactory:
    ERROR_MESSAGE_INVALID_LIMIT = "limit must be greater than 0"
    ERROR_MESSAGE_INVALID_OFFSET = "offset must be greater than equal 0"

    KEY_LIMIT = "limit"
    KEY_OFFSET = "offset"

    def create_pagination(self, param_dict: dict) -> Pagination:
        limit = param_dict.get(self.KEY_LIMIT)
        offset = param_dict.get(self.KEY_OFFSET)

        return self._create_pagination(limit, offset)

    def create_one_pagination(self) -> Pagination:
        limit = 1
        offset = 0
        return self._create_pagination(limit, offset)

    def _create_pagination(self, limit: Optional[int], offset: Optional[int]) -> Pagination:
        if limit is None:
            limit = 10
        if offset is None:
            offset = 0
        if limit < 0:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_MESSAGE_INVALID_LIMIT)
        if offset < 0:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_MESSAGE_INVALID_OFFSET)

        return Pagination(limit=limit, offset=offset)
