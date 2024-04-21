import uuid
from typing import Optional, List

import bson

from app.common.error import ErrorCode, BizException, EzErrorCodeEnum
from app.domain.lowcode_model.dsl.dsl_param import Selector, SelectorFactory, Pagination, PaginationFactory, \
    IncludeContextFactory, IncludeContext, DSLParamDict, OrderByFactory, OrderBy
from app.domain.lowcode_model.dsl.node.factory import NodeFactory
from app.domain.lowcode_model.dsl.node.node_base import WhereNode
from app.domain.lowcode_model.model_ctx.model import ModelContext, MetadataContext


class FindDomain:
    def __init__(self, *, selector: Selector, pagination: Pagination, where_node: WhereNode,
                 with_count=False, include_context: IncludeContext = None, orderby: OrderBy = None):
        self.selector = selector
        self.pagination = pagination
        self.where_node = where_node
        self.with_count = with_count
        self.include_context = include_context
        self.orderby: OrderBy = orderby

    @property
    def need_include(self):
        return self.include_context is not None and self.include_context.need_include


class FindManyDomain:
    def __init__(self, *, selector: Selector, pagination: Pagination, where_node: WhereNode,
                 with_count=False, include_context: IncludeContext = None, orderby: OrderBy = None):
        self.selector = selector
        self.pagination = pagination
        self.where_node = where_node
        self.with_count = with_count
        self.include_context = include_context
        self.orderby: OrderBy = orderby

    @property
    def need_include(self):
        return self.include_context is not None and self.include_context.need_include


class CreateDomain:
    def __init__(self, *, data: dict, insert_id: str):
        self.data = data
        self.insert_id = insert_id


class CreateManyDomain:
    def __init__(self, datalist: List[dict], insert_id_list: List):
        self.datalist = datalist
        self.insert_id_list = insert_id_list


class UpdateDomain:
    def __init__(self, where: WhereNode, data: dict):
        self.where = where
        self.__data = data

    @property
    def query(self):
        return self.where.to_dict()

    @property
    def data(self):
        return self.__data


class UpdateManyDomain:
    def __init__(self, where: WhereNode, data: dict):
        self.where = where
        self.__data = data

    @property
    def query(self):
        return self.where.to_dict()

    @property
    def data(self):
        return self.__data


class DeleteDomain:
    def __init__(self, where: WhereNode, unique: bool = False):
        self.where = where
        self.unique = unique

    @property
    def query(self):
        return self.where.to_dict()


class DeleteManyDomain:
    def __init__(self, where: WhereNode):
        self.where = where

    @property
    def query(self):
        return self.where.to_dict()


def generate_id() -> str:
    return bson.ObjectId().__str__()


class DomainFactory:
    def __init__(self, model_context: ModelContext):
        self.model_context = model_context
        self.selector_factory = SelectorFactory(model_ctx=model_context)
        self.pagination_factory = PaginationFactory()
        self.node_factory = NodeFactory()
        self.include_factory = IncludeContextFactory(model_ctx=model_context)
        self.orderby_factory = OrderByFactory(model_ctx=model_context)

    KEY_WITH_COUNT = "withCount"
    KEY_DATA = "data"
    KEY_WHERE = "where"
    KEY_LIMIT = "limit"
    KEY_UNIQUE = "unique"

    ERROR_INVALID_DATALIST_VALUE = "value `data` should be List[dict], reference : {'datalist':[{'foo':'bar'}]}"
    ERROR_PARAM_IS_NONE = "param can not be none"
    ERROR_DATA_VALUE_IS_NONE = "data value can not be none when using method 'create'"
    ERROR_SELECT_AND_INCLUDE_BOTH_EXIST = "Please either use `include` or `select`, but not both at the same time."

    EXAMPLE_CREATE_ONE = '{"data":{"name":"foo", "age":18}}'
    EXAMPLE_CREATE_MANY = '{"data":[{"name":"foo", "age":18}]}'
    EXAMPLE_UPDATE_ONE = '{"where":{"name":"foo"}, "data":{"name":"foo", "age":18}}'
    EXAMPLE_UPDATE_MANY = '{"where":{"name":"foo"}, "data":{"name":"foo", "age":18}}'
    EXAMPLE_DELETE_ONE = '{"where":{"name":"foo"}, "checkUnique":true}'
    EXAMPLE_DELETE_MANY = '{"where":{"name":"foo"}}'

    def __with_count(self, param: dict) -> bool:
        return param.get(self.KEY_WITH_COUNT, False)

    def __limit(self, param: dict) -> Optional[int]:
        return param.get(self.KEY_LIMIT, None)

    def __get_unique(self, param: dict) -> bool:
        value = param.get(self.KEY_UNIQUE, False)
        if value is None:
            return False
        else:
            return value

    def find_domain(self, *, param: DSLParamDict) -> FindDomain:
        self.check_valid_find_param(param)
        selector = self.selector_factory.create_selector(param)
        pagination = self.pagination_factory.create_one_pagination()
        where_node = self.node_factory.create_node(param)
        with_count = self.__with_count(param)
        include_context = self.include_factory.create_include_context(param=param)
        orderby = self.orderby_factory.create_order_by(param=param)
        return FindDomain(
            selector=selector,
            pagination=pagination,
            where_node=where_node,
            with_count=with_count,
            include_context=include_context,
            orderby=orderby,
        )

    @classmethod
    def check_valid_find_param(cls, param):
        if ("select" in param and param.get('select') is not None and
                "include" in param and param.get('include') is not None):
            raise BizException(ErrorCode.InvalidParameter, cls.ERROR_SELECT_AND_INCLUDE_BOTH_EXIST)

    def find_many_domain(self, *, param: dict) -> FindManyDomain:
        self.check_valid_find_param(param)
        selector = self.selector_factory.create_selector(param)
        pagination = self.pagination_factory.create_pagination(param)
        where_node = self.node_factory.create_node(param)
        with_count = self.__with_count(param)
        include_context = self.include_factory.create_include_context(param=param)
        orderby = self.orderby_factory.create_order_by(param=param)
        return FindManyDomain(
            selector=selector,
            pagination=pagination,
            where_node=where_node,
            with_count=with_count,
            include_context=include_context,
            orderby=orderby,
        )

    def create_domain(self, *, param: Optional[dict], metadata_ctx: MetadataContext = None) -> CreateDomain:
        if param is None:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        if self.KEY_DATA not in param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_DATA, self.EXAMPLE_CREATE_ONE])
        data = param[self.KEY_DATA]
        if not isinstance(data, dict):
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)

        if metadata_ctx is not None:
            metadata_ctx.validate_on_create(data)
        insert_id = self.process_sys_fields(data=data)
        return CreateDomain(data=data, insert_id=insert_id)

    def create_many_domain(self, *, param: Optional[dict],
                           metadata_ctx: MetadataContext = None) -> CreateManyDomain:
        if param is None:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        if self.KEY_DATA not in param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_DATA, self.EXAMPLE_CREATE_MANY])
        data: list = param[self.KEY_DATA]
        if not isinstance(data, list):
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_INVALID_DATALIST_VALUE)
        if metadata_ctx is not None:
            metadata_ctx.validate_on_create_many(data)
        insert_id_list = []
        for data_elem in data:
            if data_elem is None:
                continue
            insert_id_list.append(self.process_sys_fields(data=data_elem))
        # todo filter key by model_context
        return CreateManyDomain(datalist=data, insert_id_list=insert_id_list)

    def update_domain(self, *, param) -> UpdateDomain:
        example = self.EXAMPLE_UPDATE_ONE
        if param is None:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        if self.KEY_DATA not in param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_DATA, example])
        data = param[self.KEY_DATA]
        if self.KEY_WHERE not in param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_WHERE, example])
        if not isinstance(data, dict):
            raise BizException(ezcode=EzErrorCodeEnum.InvalidTypeOfValue,
                               arg_list=[self.KEY_DATA, 'dict', example])
        # todo filter key by model_context
        where_node = self.node_factory.create_node(param)
        return UpdateDomain(where=where_node, data=data)

    def update_many_domain(self, *, param) -> UpdateManyDomain:
        example = self.EXAMPLE_UPDATE_MANY
        if param is None:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        if self.KEY_DATA not in param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_DATA, example])
        data = param[self.KEY_DATA]
        if self.KEY_WHERE not in param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_WHERE, example])
        if not isinstance(data, dict):
            raise BizException(ezcode=EzErrorCodeEnum.InvalidTypeOfValue,
                               arg_list=[self.KEY_DATA, 'dict', example])
        # todo filter key by model_context
        where_node = self.node_factory.create_node(param)
        return UpdateManyDomain(where=where_node, data=data)

    def delete_domain(self, *, param):
        example = self.EXAMPLE_DELETE_ONE
        if param is None:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        if self.KEY_WHERE not in param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_WHERE, example])
        where_node = self.node_factory.create_node(param)
        unique = self.__get_unique(param)
        return DeleteDomain(where=where_node, unique=unique)

    def delete_many_domain(self, *, param):
        example = self.EXAMPLE_DELETE_MANY
        if param is None:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        if self.KEY_WHERE not in param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_WHERE, example])
        where_node = self.node_factory.create_node(param)
        return DeleteManyDomain(where=where_node)

    def process_sys_fields(self, *, data: dict) -> str:
        if data is None:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_DATA_VALUE_IS_NONE)
        if "id" not in data or data["id"] is None:
            insert_id = generate_id()
            data["id"] = insert_id
            return insert_id
