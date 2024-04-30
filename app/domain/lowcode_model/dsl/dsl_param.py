from dataclasses import dataclass
from typing import Dict, Union, Optional, List, TypedDict, Tuple

from app.common.bizlogger import LOGGER
from app.common.decorator import readable
from app.common.error import BizException, ErrorCode
from app.domain.lowcode_model.model_ctx.column import RelationInfo, ColumnFormat, SchemaColumn
from app.domain.lowcode_model.model_ctx.model import MetadataContext, ModelContext

"""
dsl option

selector

pagination

include
"""


class DSLParamDict(TypedDict, total=False):
    select: dict
    where: dict
    include: dict
    limit: int
    offset: int
    orderby: List[dict]


@readable
class Selector:
    def __init__(self, *, select_dict: dict, find_all=False):
        if select_dict is None:
            select_dict = {}
        self.select_dict = select_dict
        self.find_all = find_all


class SelectorFactory:
    """
    Args:
        1. model_contex (model.ModelContext) : 模型上下文
    """

    def __init__(self, *, model_ctx: ModelContext):
        self.model_ctx: ModelContext = model_ctx

    def create_all_selector(self, model_name: str = None):
        new_dict = self.select_all(model_name=model_name)
        find_all = True
        return Selector(select_dict=new_dict, find_all=find_all)

    def create_selector(self, select_dict: DSLParamDict, model_name: str = None):
        new_dict = {}
        find_all = False
        if 'select' not in select_dict:
            # select all
            new_dict = self.select_all(model_name=model_name)
            find_all = True
        else:
            new_dict = self.select_target(select_dict['select'])
        return Selector(select_dict=new_dict, find_all=find_all)

    def select_all(self, model_name: str = None) -> Dict[str, Union[int, Dict]]:
        new_select_dict: Dict[str, Union[int, Dict[str, 1]]] = {}
        if model_name is None or model_name == '':
            model_name = self.model_ctx.model_name_ctx.name
        metadata_ctx: MetadataContext = self.model_ctx.get_metadata_ctx_by_name(model_name=model_name)
        if metadata_ctx is None:
            raise BizException(ErrorCode.InvalidParameter, f"MetadataContext not found model_name={model_name}")

        column_list: List[SchemaColumn] = metadata_ctx.column_list
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

    def select_target(self, select_dict: dict) -> Dict[str, Union[int, Dict]]:
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

    def create_pagination(self, param: DSLParamDict) -> Pagination:
        limit = param.get('limit')
        offset = param.get('offset')

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
    def __init__(self, *, local_key: str, foreign_key: str, from_col_name: str, include_as_key: str,
                 selector: Selector, join_one: bool = False):
        self.local_key: str = local_key
        self.foreign_key: str = foreign_key
        self.from_col_name: str = from_col_name
        self.include_as_key: str = include_as_key
        self.selector: Selector = selector
        self.join_one: bool = join_one

    def to_mongo_cmd_list(self) -> List[dict]:
        # 获取mongo的lookup查询
        cmd_list = []
        related_select: dict = self.selector.select_dict
        related_select['_id'] = 0
        lookup: dict = {
            "$lookup": {
                "from": self.from_col_name,
                "let": {
                    "local_field": f"${self.local_key}"
                },
                "pipeline": [
                    {"$match":
                        {
                            "$expr":
                                {"$eq": ["$$local_field", f"${self.foreign_key}"]}
                        }
                    },
                    {"$project": related_select},
                ],
                "as": self.include_as_key
            }
        }
        cmd_list.append(lookup)
        # 如果是多对一，就返回单文档
        if self.join_one:
            cmd_list.append({
                "$unwind": '$' + self.include_as_key
            })
        # 否则返回数组，就不需要$unwind
        return cmd_list


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
        self.selector_factory: SelectorFactory = SelectorFactory(model_ctx=self.model_ctx)

    def create_include_context(self, *, param: DSLParamDict) -> IncludeContext:
        if 'include' not in param or param['include'] is None:
            return IncludeContext.create_none_include_context()

        include_dict = param['include']
        if not isinstance(include_dict, dict):
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_INCLUDE_MUST_BE_DICT)

        if len(include_dict.items()) == 0:
            return IncludeContext.create_none_include_context()

        metadata_ctx: MetadataContext = self.model_ctx.get_master_metadata_ctx()
        relation_column_list: List[SchemaColumn] = metadata_ctx.relation_column_list

        def need_process_relation(column: SchemaColumn) -> bool:
            if column.name in include_dict:
                include_value = include_dict[column.name]
                if include_value is True:
                    return True
            return False

        valid_relation_column_list = [column for column in relation_column_list if need_process_relation(column)]

        if len(valid_relation_column_list) == 0:
            return IncludeContext.create_none_include_context()

        include_param_list: List[IncludeParam] = []
        for column in relation_column_list:
            include_param = self.column_2_include_param(column=column, include_dict_param=include_dict)
            if include_param is not None:
                include_param_list.append(include_param)

        return IncludeContext(need_include=True, include_param_list=include_param_list)

    def column_2_include_param(self, column: SchemaColumn, include_dict_param: dict) -> Optional[IncludeParam]:
        relation_info: RelationInfo = column.get_relation()
        LOGGER.debug(f"relation_info={relation_info}, include_dict={include_dict_param}")
        include_dict_value = include_dict_param.get(column.name)
        if include_dict_value is None:
            return None
        if include_dict_value:
            selector = self.selector_factory.create_all_selector(relation_info['relatedModelName'])
        else:
            selector = self.selector_factory.create_selector(select_dict=include_dict_value)
        include_param = IncludeParam(
            local_key=relation_info['field'],
            foreign_key=relation_info['relatedField'],
            from_col_name=relation_info['relatedModelName'],
            include_as_key=column.name,
            selector=selector,
            join_one=column.column_format == ColumnFormat.MANY_TO_ONE
        )
        return include_param


class OrderBy:
    def __init__(self, order_by_list: List = None):
        self.order_by_list: List[Tuple[str, int]] = order_by_list


class OrderByFactory:
    def __init__(self, model_ctx: ModelContext):
        self.model_ctx = model_ctx

    def create_order_by(self, *, param: DSLParamDict) -> OrderBy:
        if 'orderby' not in param or param['orderby'] is None:
            return OrderBy()
        orderby_value = param['orderby']
        if not isinstance(orderby_value, list):
            raise BizException(ErrorCode.InvalidParameter, 'orderby must be a list')
        orderby_list = []
        for value in orderby_value:
            orderby_tuple = self.get_orderby(value)
            if orderby_tuple:
                orderby_list.append(orderby_tuple)

        orderby_list = [self.get_orderby(value) for value in orderby_value]
        return OrderBy(order_by_list=orderby_list)

    def get_orderby(self, one_orderby: dict) -> Optional[Tuple]:
        if not isinstance(one_orderby, dict):
            return None
        keys = list(one_orderby.keys())
        if len(keys) == 0:
            return None
        if len(keys) > 1:
            raise BizException(ErrorCode.InvalidParameter, 'orderby must be [{"a":1}], each dict can only have one key')
        first_key = keys[0]
        return first_key, 1 if one_orderby[first_key] > 0 else -1
