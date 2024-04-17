import unittest
from unittest.mock import Mock

from app.common import utils
from app.domain.lowcode_model.dsl.dsl_domain import DomainFactory
from app.domain.lowcode_model.dsl.dsl_param import SelectorFactory, PaginationFactory
from app.domain.lowcode_model.dsl.node.factory import NodeFactory
from app.domain.lowcode_model.model_ctx.model import ModelContext


class TestFindDomain(unittest.TestCase):

    def setUp(self):
        self.model_context = ModelContext.create_from_schema(self.example_schema)
        self.selector_factory = Mock(SelectorFactory)
        self.pagination_factory = Mock(PaginationFactory)
        self.node_factory = Mock(NodeFactory)

        self.domain_factory = DomainFactory(self.model_context)

    def test_find_domain(self):
        # Arrange
        dict_param = {
            'select': {'id': 1, 'name': 1},
            'limit': 10,
            'offset': 0,
            'where': {'name': 'value1'}
        }

        result = self.domain_factory.find_domain(dict_param)
        print(result.selector)
        print(result.pagination)
        print(result.where_node.to_dict())

    def test_find_many_domain(self):
        # Arrange
        dict_param = {
            'select': {'id': 1, 'name': 1},
            'limit': 10,
            'offset': 0,
            'where': {'name': 'value1'}
        }

        result = self.domain_factory.find_many_domain(dict_param)
        print(result.selector)
        print(result.pagination)
        print(result.where_node.to_dict())

    def test_create_domain(self):
        dict_param = {
            'data': {
                'id': '1',
                'name': 'abcdefg',
            }
        }
        domain = self.domain_factory.create_domain(dict_param=dict_param)
        print(domain)

    def test_create_many_domain(self):
        dict_param = {
            'data': [{
                'id': '1',
                'name': 'abcdefg',
            }]
        }
        domain = self.domain_factory.create_many_domain(dict_param=dict_param)
        print(domain)

    def test_update_domain(self):
        dict_param = {
            'where': {'name': 'value1'},
            'data': {
                'id': '1',
                'name': 'abcdefg',
            }
        }
        domain = self.domain_factory.update_domain(dict_param=dict_param)
        print(utils.toJSON(domain))

    def test_update_many_domain(self):
        dict_param = {
            'where': {'name': 'value1'},
            'limit': 5,
            'data': {
                'id': '1',
                'name': 'abcdefg',
            }
        }
        domain = self.domain_factory.update_many_domain(dict_param=dict_param)
        print(utils.toJSON(domain))

        dict_param = {
            'where': {'name': 'value1'},
            'data': {
                'id': '1',
                'name': 'abcdefg',
            }
        }
        domain = self.domain_factory.update_many_domain(dict_param=dict_param)

    def test_delete(self):
        # Arrange
        dict_param = {
            'where': {'name': 'value1'}
        }

        result = self.domain_factory.delete_domain(dict_param=dict_param)
        print(result.query)

    def test_delete_many(self):
        # Arrange
        dict_param = {
            'where': {'name': 'value1'}
        }

        result = self.domain_factory.delete_many_domain(dict_param=dict_param)
        print(result.query)


if __name__ == '__main__':
    unittest.main()
