import unittest
from unittest.mock import Mock
from app.service.model_domain.dsl.node.factory import NodeFactory
from app.service.model_domain.dsl.node.node_base import WhereNode
from app.service.model_domain.dsl.pagination import Pagination, PaginationFactory
from app.service.model_domain.dsl.select import Selector, SelectorFactory
from app.service.model_domain.dsl.find_domain import FindDomain, FindParam, FindDomainFactory
from app.service.model_domain.metadata.model import ModelContext


class TestFindDomain(unittest.TestCase):
    example_schema = {"type": "object",
                      "properties": {
                          "id": {"type": "integer", "x-format": "x-short-text"},
                          "name": {"type": "number", "x-format": "x-number"},
                          "relation": {"type": "number", "x-format": "x-many-to-one"}
                      }
                      }

    def setUp(self):
        self.model_context = ModelContext.create_from_schema(self.example_schema)
        self.selector_factory = Mock(SelectorFactory)
        self.pagination_factory = Mock(PaginationFactory)
        self.node_factory = Mock(NodeFactory)

        self.find_domain_factory = FindDomainFactory(self.model_context)

    def test_create_find_domain(self):
        # Arrange
        dict_param = {
            'select': {'id': 1, 'name': 1},
            'limit': 10,
            'offset': 0,
            'where': {'name': 'value1'}
        }

        result = self.find_domain_factory.create_find_domain(dict_param)
        print(result.selector)
        print(result.pagination)
        print(result.where_node.to_dict())


if __name__ == '__main__':
    unittest.main()
