import unittest
from unittest.mock import MagicMock

from app.common.error import ErrorCode, BizException
from app.domain.lowcode_model.model_ctx.field import SchemaColumn
from app.domain.lowcode_model.model_ctx.model import MetadataContext
from .dsl_param import Selector, SelectorFactory, PaginationFactory, IncludeContextFactory
from ..model_ctx import model


class TestSelector(unittest.TestCase):

    def test_init(self):
        select_dict = {'a': 1, 'b': 1, 'c': 0, 'sub_table': {'sub_a': 1, 'sub_b': 1}}
        selector = Selector(select_dict=select_dict)
        self.assertEqual(selector.select_dict, select_dict)


class TestSelectorFactory(unittest.TestCase):

    def setUp(self):
        self.model_context = MagicMock(spec=model.ModelContext)
        self.metadata_ctx = MagicMock(model.MetadataContext)
        self.metadata_ctx.column_list = [
            SchemaColumn(key='a', json_val={'name': 'a'}),
            SchemaColumn(key='b', json_val={'name': 'b'}),
            SchemaColumn(key='c', json_val={'name': 'c'})
        ]
        self.model_context.get_master_metadata_ctx.return_value = self.metadata_ctx
        self.selector_factory = SelectorFactory(self.model_context)

    def test_func(self):
        mtx = self.model_context.get_master_metadata_ctx()
        print(mtx)
        print(mtx.column_list)
        pass

    def test_create_selector(self):
        select_dict = {'select': {'a': 1, 'b': 1, 'c': 0, 'sub_table': {'sub_a': 1, 'sub_b': 1}}}
        expect_dict = {'a': 1, 'b': 1, 'sub_table': {'sub_a': 1, 'sub_b': 1}}
        selector = self.selector_factory.create_selector(select_dict)
        print(selector.select_dict)
        self.assertIsInstance(selector, Selector)
        self.assertEqual(expect_dict, selector.select_dict)

    def test_select_all(self):
        expected_result = {'a': 1, 'b': 1, 'c': 1}

        selector = self.selector_factory.create_selector({})
        print(selector.select_dict)
        self.assertIsInstance(selector, Selector)
        self.assertTrue(selector.find_all)
        self.assertEqual(expected_result, selector.select_dict)

    def test_filter_non_zero(self):
        input_dict = {'a': 1, 'b': 0, 'c': 1, 'sub_table': {'sub_a': 0, 'sub_b': 1}}
        result = self.selector_factory.filter_non_zero(input_dict)
        expected_result = {'a': 1, 'c': 1, 'sub_table': {'sub_b': 1}}
        self.assertEqual(result, expected_result)


class TestPaginationFactory(unittest.TestCase):
    def setUp(self):
        self.factory = PaginationFactory()

    def test_create_pagination_with_valid_params(self):
        param_dict = {"limit": 5, "offset": 10}
        pagination = self.factory.create_pagination(param_dict)
        self.assertEqual(pagination.limit, 5)
        self.assertEqual(pagination.offset, 10)

    def test_create_pagination_with_invalid_limit(self):
        param_dict = {"limit": -5, "offset": 10}
        with self.assertRaises(BizException) as context:
            self.factory.create_pagination(param_dict)
        self.assertEqual(context.exception.code, ErrorCode.InvalidParameter.value)
        self.assertEqual(context.exception.message, PaginationFactory.ERROR_MESSAGE_INVALID_LIMIT)

    def test_create_pagination_with_invalid_offset(self):
        param_dict = {"limit": 5, "offset": -10}
        with self.assertRaises(BizException) as context:
            self.factory.create_pagination(param_dict)
        self.assertEqual(context.exception.code, ErrorCode.InvalidParameter.value)
        self.assertEqual(context.exception.message, PaginationFactory.ERROR_MESSAGE_INVALID_OFFSET)

    def test_create_pagination_with_default_values(self):
        param_dict = {}
        pagination = self.factory.create_pagination(param_dict)
        self.assertEqual(pagination.limit, 10)
        self.assertEqual(pagination.offset, 0)

    def test_create_pagination_default_values(self):
        pagination = self.factory._create_pagination(None, None)
        self.assertEqual(pagination.limit, 10)
        self.assertEqual(pagination.offset, 0)

    def test_create_pagination_custom_values(self):
        pagination = self.factory._create_pagination(5, 20)
        self.assertEqual(pagination.limit, 5)
        self.assertEqual(pagination.offset, 20)

    def test_create_pagination_invalid_limit(self):
        with self.assertRaises(BizException) as context:
            self.factory._create_pagination(-1, 10)
        self.assertEqual(context.exception.code, ErrorCode.InvalidParameter.value)
        self.assertEqual(context.exception.message, PaginationFactory.ERROR_MESSAGE_INVALID_LIMIT)

    def test_create_pagination_invalid_offset(self):
        with self.assertRaises(BizException) as context:
            self.factory._create_pagination(10, -1)
        self.assertEqual(context.exception.code, ErrorCode.InvalidParameter.value)
        self.assertEqual(context.exception.message, PaginationFactory.ERROR_MESSAGE_INVALID_OFFSET)


class TestIncludeParams(unittest.TestCase):
    def setUp(self):
        self.model_context = MagicMock(spec=model.ModelContext)
        self.metadata_ctx = MagicMock(model.MetadataContext)
        self.metadata_ctx.relation_column_list = [
            SchemaColumn(
                key='relation',
                json_val={
                    'name': 'c',
                    'format': 'xManyToOne',
                    'xRelation': {
                        'field': "userId",
                        'relatedField': '_id',
                        'relatedModelName': 'user',
                    }}),
        ]
        self.model_context.get_master_metadata_ctx.return_value = self.metadata_ctx
        self.factory = IncludeContextFactory(model_ctx=self.model_context)

    def test_metadata_ctx(self):
        metadata_ctx: MetadataContext = self.model_context.get_master_metadata_ctx()
        list = metadata_ctx.relation_column_list
        print(list)

    def test_include_false(self):
        include_ctx = self.factory.create_include_context(param_dict={})

        self.assertTrue(not include_ctx.need_include)

    def test_include_invalid(self):
        with self.assertRaises(BizException) as context:
            include_ctx = self.factory.create_include_context(param_dict={"include": []})
        self.assertEqual(context.exception.code, ErrorCode.InvalidParameter.value)
        self.assertEqual(context.exception.message, IncludeContextFactory.ERROR_INCLUDE_MUST_BE_DICT)

    def test_include_false_with_empty_dict(self):
        include_ctx = self.factory.create_include_context(param_dict={"include": {}})

        self.assertTrue(not include_ctx.need_include)

    def test_include_right_with_key_not_in_metadata(self):
        # include 包含的key
        include_ctx = self.factory.create_include_context(param_dict={"include": {"posts": True}})

        self.assertTrue(not include_ctx.need_include)

    def test_include_right_with_key_in_metadata(self):
        # include 包含的key
        include_ctx = self.factory.create_include_context(param_dict={"include": {"relation": True}})

        self.assertTrue(include_ctx.need_include)
        print(include_ctx)


if __name__ == '__main__':
    unittest.main()
