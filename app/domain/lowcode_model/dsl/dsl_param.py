from dataclasses import dataclass
from typing import Dict, Union, Optional, List, TypedDict

from app.common.decorator import readable
from app.common.error import BizException, ErrorCode
from app.domain.lowcode_model.model_ctx import model, field
from app.domain.lowcode_model.model_ctx.field import RelationInfo
from app.domain.lowcode_model.model_ctx.model import MetadataContext, ModelContext

"""
dsl option

selector

pagination

include
"""


class DSLParamKey(TypedDict, total=False):
    select: str
    include: str
    limit: str
    offset: str


DSL_PARAM_KEY: DSLParamKey = {
    'select': 'select',
    'include': 'include',
    'limit': "limit",
    'offset': "offset",
}


@readable
class Selector:
    def __init__(self, *, select_dict: dict, find_all=False):
        self.select_dict = select_dict
        self.find_all = find_all


class SelectorFactory:
    """
    Args:
        1. model_contex (model.ModelContext) : 模型上下文
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
        find_all = False
        key_select = DSL_PARAM_KEY['select']
        if key_select not in select_dict:
            # select all
            new_dict = self.select_all()
            find_all = True
        else:
            new_dict = self.select_target(select_dict[key_select])
        return Selector(select_dict=new_dict, find_all=find_all)

    def select_all(self) -> Dict[str, Union[int, Dict]]:
        new_select_dict: Dict[str, Union[int, Dict[str, 1]]] = {}
        master_metadata_ctx: MetadataContext = self.model_context.get_master_metadata_ctx()
        column_list: List[field.SchemaColumn] = master_metadata_ctx.column_list
        print(column_list)
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

    def create_pagination(self, param_dict: dict) -> Pagination:
        limit = param_dict.get(DSL_PARAM_KEY['limit'])
        offset = param_dict.get(DSL_PARAM_KEY['offset'])

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


@readable
class IncludeParam:
    def __init__(self, *, local_key: str, foreign_key: str, from_col_name: str, include_as_key: str):
        self.local_key: str = local_key
        self.foreign_key: str = foreign_key
        self.from_col_name: str = from_col_name
        self.include_as_key: str = include_as_key


@readable
class IncludeContext:
    def __init__(self, *, need_include: bool = False, include_param_list: List[IncludeParam] = None):
        if include_param_list is None:
            include_param_list = []
        self.need_include: bool = need_include
        self.include_param_list: List[IncludeParam] = include_param_list

    @staticmethod
    def create_none_include_context() -> "IncludeContext":
        return IncludeContext(need_include=False)


class IncludeContextFactory:
    """
    {
      "include":{
         "posts":true
      }
    }
    posts 是一个关联字段， 当你这么使用时，就会携带关联字段出来。
    """
    ERROR_INCLUDE_MUST_BE_DICT = "include must be a dict"

    def __init__(self, *, model_ctx: ModelContext):
        self.model_ctx: ModelContext = model_ctx
        pass

    def create_include_context(self, *, param_dict: dict) -> IncludeContext:
        key_include = DSL_PARAM_KEY['include']
        if key_include not in param_dict:
            return IncludeContext.create_none_include_context()

        include_dict = param_dict[key_include]
        if not isinstance(include_dict, dict):
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_INCLUDE_MUST_BE_DICT)

        if len(include_dict.items()) == 0:
            return IncludeContext.create_none_include_context()

        metadata_ctx: MetadataContext = self.model_ctx.get_master_metadata_ctx()
        relation_column_list: List[field.SchemaColumn] = metadata_ctx.relation_column_list

        def need_process_relation(column: field.SchemaColumn) -> bool:
            if column.name in include_dict:
                include_value = include_dict[column.name]
                if include_value is True:
                    return True
            return False

        valid_relation_column_list = [column for column in relation_column_list if need_process_relation(column)]

        if len(valid_relation_column_list) == 0:
            return IncludeContext.create_none_include_context()

        def column_2_include_param(column: field.SchemaColumn) -> IncludeParam:
            relation_info: RelationInfo = column.get_relation()
            include_param = IncludeParam(
                local_key=relation_info['field'],
                foreign_key=relation_info['relatedField'],
                from_col_name=relation_info['relatedModelName'],
                include_as_key=column.name,
            )
            return include_param

        include_param_list: List[IncludeParam] = \
            [column_2_include_param(column) for column in valid_relation_column_list]
        return IncludeContext(need_include=True, include_param_list=include_param_list)
