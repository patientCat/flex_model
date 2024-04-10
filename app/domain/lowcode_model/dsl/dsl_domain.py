from typing import Optional, List

from app.common.error import ErrorCode, BizException, EzErrorCodeEnum
from app.domain.lowcode_model.dsl.dsl_param import Selector, SelectorFactory, Pagination, PaginationFactory
from app.domain.lowcode_model.dsl.node.factory import NodeFactory
from app.domain.lowcode_model.dsl.node.node_base import WhereNode
from app.domain.lowcode_model.model_ctx.model import ModelContext


class FindDomain:
    def __init__(self, selector: Selector, pagination: Pagination, where_node: WhereNode, with_count=False):
        self.selector = selector
        self.pagination = pagination
        self.where_node = where_node
        self.with_count = with_count


class FindManyDomain:
    def __init__(self, selector: Selector, pagination: Pagination, where_node: WhereNode, with_count=False):
        self.selector = selector
        self.pagination = pagination
        self.where_node = where_node
        self.with_count = with_count


class CreateDomain:
    def __init__(self, data: dict):
        self.data = data


class CreateManyDomain:
    def __init__(self, datalist: List[dict]):
        self.datalist = datalist


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


class DomainFactory:
    def __init__(self, model_context: ModelContext):
        self.model_context = model_context
        self.selector_factory = SelectorFactory(model_context)
        self.pagination_factory = PaginationFactory()
        self.node_factory = NodeFactory()

    KEY_WITH_COUNT = "withCount"
    KEY_DATA = "data"
    KEY_WHERE = "where"
    KEY_LIMIT = "limit"

    ERROR_INVALID_DATALIST_VALUE = "value `data` should be List[dict], reference : {'datalist':[{'foo':'bar'}]}"
    ERROR_PARAM_IS_NONE = "param can not be none"
    EXAMPLE_CREATE_ONE = '{"data":{"name":"foo", "age":18}}'
    EXAMPLE_CREATE_MANY = '{"data":[{"name":"foo", "age":18}]}'
    EXAMPLE_UPDATE_ONE = '{"where":{"name":"foo"}, "data":{"name":"foo", "age":18}}'
    EXAMPLE_UPDATE_MANY = '{"where":{"name":"foo"}, "data":{"name":"foo", "age":18}}'

    def __with_count(self, dict_param: dict) -> bool:
        return dict_param.get(self.KEY_WITH_COUNT, False)

    def __limit(self, dict_param: dict) -> Optional[int]:
        return dict_param.get(self.KEY_LIMIT, None)

    def find_domain(self, dict_param: dict) -> FindDomain:
        selector = self.selector_factory.create_selector(dict_param)
        pagination = self.pagination_factory.create_one_pagination()
        where_node = self.node_factory.create_node(dict_param)
        with_count = self.__with_count(dict_param)
        return FindDomain(selector, pagination, where_node, with_count)

    def find_many_domain(self, dict_param: dict) -> FindManyDomain:
        selector = self.selector_factory.create_selector(dict_param)
        pagination = self.pagination_factory.create_pagination(dict_param)
        where_node = self.node_factory.create_node(dict_param)
        with_count = self.__with_count(dict_param)
        return FindManyDomain(selector, pagination, where_node, with_count)

    def create_domain(self, dict_param: Optional[dict]) -> CreateDomain:
        if dict_param is None:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        if self.KEY_DATA not in dict_param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_DATA, self.EXAMPLE_CREATE_ONE])
        data = dict_param[self.KEY_DATA]
        if not isinstance(data, dict):
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        # todo filter key by model_context
        return CreateDomain(data=data)

    def create_many_domain(self, dict_param: Optional[dict]) -> CreateManyDomain:
        if dict_param is None:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        if self.KEY_DATA not in dict_param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_DATA, self.EXAMPLE_CREATE_MANY])
        data = dict_param[self.KEY_DATA]
        if not isinstance(data, list):
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_INVALID_DATALIST_VALUE)
        # todo filter key by model_context
        return CreateManyDomain(datalist=data)

    def update_domain(self, dict_param) -> UpdateDomain:
        example = self.EXAMPLE_UPDATE_ONE
        if dict_param is None:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        if self.KEY_DATA not in dict_param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_DATA, example])
        data = dict_param[self.KEY_DATA]
        if self.KEY_WHERE not in dict_param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_WHERE, example])
        if not isinstance(data, dict):
            raise BizException(ezcode=EzErrorCodeEnum.InvalidTypeOfValue,
                               arg_list=[self.KEY_DATA, 'dict', example])
        # todo filter key by model_context
        where_node = self.node_factory.create_node(dict_param)
        return UpdateDomain(where=where_node, data=data)

    def update_many_domain(self, dict_param) -> UpdateManyDomain:
        example = self.EXAMPLE_UPDATE_MANY
        if dict_param is None:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_PARAM_IS_NONE)
        if self.KEY_DATA not in dict_param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_DATA, example])
        data = dict_param[self.KEY_DATA]
        if self.KEY_WHERE not in dict_param:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound,
                               arg_list=[self.KEY_WHERE, example])
        if not isinstance(data, dict):
            raise BizException(ezcode=EzErrorCodeEnum.InvalidTypeOfValue,
                               arg_list=[self.KEY_DATA, 'dict', example])
        # todo filter key by model_context
        where_node = self.node_factory.create_node(dict_param)
        return UpdateManyDomain(where=where_node, data=data)
