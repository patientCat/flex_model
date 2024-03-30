from typing import TypedDict

from app.service.model_domain.dsl.node.factory import NodeFactory
from app.service.model_domain.dsl.node.node_base import WhereNode
from app.service.model_domain.dsl.pagination import Pagination, PaginationFactory
from app.service.model_domain.dsl.select import Selector, SelectorFactory
from app.service.model_domain.metadata.model import ModelContext


class FindDomain:
    def __init__(self, selector: Selector, pagination: Pagination, where_node: WhereNode):
        self.selector = selector
        self.pagination = pagination
        self.where_node = where_node


class FindParam(TypedDict):
    select: str
    limit: int
    offset: int
    where: dict


class FindDomainFactory:
    def __init__(self, model_context: ModelContext):
        self.model_context = model_context
        self.selector_factory = SelectorFactory(model_context)
        self.pagination_factory = PaginationFactory()
        self.node_factory = NodeFactory()

    def create_find_domain(self, dict_param: dict) -> FindDomain:
        selector = self.selector_factory.create_selector(dict_param)
        pagination = self.pagination_factory.create_pagination(dict_param)
        where_node = self.node_factory.create_node(dict_param)
        return FindDomain(selector, pagination, where_node)
