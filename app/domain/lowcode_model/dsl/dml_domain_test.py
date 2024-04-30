import unittest
from unittest.mock import Mock, MagicMock

import bson

from app.common import utils
from app.common.error import BizException
from app.domain.lowcode_model.dsl.dml_domain import DmlDomainFactory
from app.domain.lowcode_model.dsl.dsl_param import SelectorFactory, PaginationFactory
from app.domain.lowcode_model.dsl.node.factory import NodeFactory
from app.domain.lowcode_model.model_ctx import model
from app.domain.lowcode_model.model_ctx.column import SchemaColumn


class TestFindDomain(unittest.TestCase):

    def setUp(self):
        self.model_context = MagicMock(spec=model.ModelContext)
        self.metadata_ctx = MagicMock(model.MetadataContext)
        self.metadata_ctx.column_list = [
            SchemaColumn(key='a', json_val={'name': 'a'}),
            SchemaColumn(key='b', json_val={'name': 'b'}),
            SchemaColumn(key='c', json_val={'name': 'c'})
        ]
        self.model_context.get_master_metadata_ctx.return_value = self.metadata_ctx
        self.selector_factory = Mock(SelectorFactory)
        self.pagination_factory = Mock(PaginationFactory)
        self.node_factory = Mock(NodeFactory)

        self.domain_factory = DmlDomainFactory(self.model_context)

    def test_find_domain(self):
        # Arrange
        param = {
            'select': {'id': 1, 'name': 1},
            'limit': 10,
            'offset': 0,
            'where': {'name': 'value1'}
        }

        result = self.domain_factory.find_domain(param=param)
        print(result.selector)
        print(result.pagination)
        print(result.where_node.to_dict())

    def test_find_conflict_select_with_include(self):
        param = {
            'select': {'id': 1, 'name': 1},
            'limit': 10,
            'offset': 0,
            'where': {'name': 'value1'},
            "include": {}
        }

        with self.assertRaises(BizException) as context:
            result = self.domain_factory.find_domain(param=param)
        self.assertEqual(context.exception.message, self.domain_factory.ERROR_SELECT_AND_INCLUDE_BOTH_EXIST)

    def test_find_many_domain(self):
        # Arrange
        param = {
            'select': {'id': 1, 'name': 1},
            'limit': 10,
            'offset': 0,
            'where': {'name': 'value1'}
        }

        result = self.domain_factory.find_many_domain(param=param)
        print(result.selector)
        print(result.pagination)
        print(result.where_node.to_dict())

    def test_get_id(self):
        id = bson.ObjectId()
        print(id)

        print(id.generation_time)
    def test_create_domain(self):
        param = {
            'data': {
                'id': '1',
                'name': 'abcdefg',
            }
        }
        domain = self.domain_factory.create_domain(param=param)
        print(domain)

    def test_create_many_domain(self):
        param = {
            'data': [{
                'id': '1',
                'name': 'abcdefg',
            }]
        }
        domain = self.domain_factory.create_many_domain(param=param)
        print(domain)

    def test_update_domain(self):
        param = {
            'where': {'name': 'value1'},
            'data': {
                'id': '1',
                'name': 'abcdefg',
            }
        }
        domain = self.domain_factory.update_domain(param=param)
        print(utils.toJSON(domain))

    def test_update_many_domain(self):
        param = {
            'where': {'name': 'value1'},
            'limit': 5,
            'data': {
                'id': '1',
                'name': 'abcdefg',
            }
        }
        domain = self.domain_factory.update_many_domain(param=param)
        print(utils.toJSON(domain))

        param = {
            'where': {'name': 'value1'},
            'data': {
                'id': '1',
                'name': 'abcdefg',
            }
        }
        domain = self.domain_factory.update_many_domain(param=param)

    def test_delete(self):
        # Arrange
        param = {
            'where': {'name': 'value1'}
        }

        result = self.domain_factory.delete_domain(param=param)
        print(result.query)

    def test_delete_many(self):
        # Arrange
        param = {
            'where': {'name': 'value1'}
        }

        result = self.domain_factory.delete_many_domain(param=param)
        print(result.query)


if __name__ == '__main__':
    unittest.main()
