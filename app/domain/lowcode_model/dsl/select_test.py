import unittest
from typing import Dict, Union
from unittest.mock import MagicMock

from app.domain.lowcode_model.model_ctx.field import SchemaColumn
from ..model_ctx import model
from .dsl_param import Selector, SelectorFactory


class TestSelector(unittest.TestCase):

    def test_init(self):
        select_dict = {'a': 1, 'b': 1, 'c': 0, 'sub_table': {'sub_a': 1, 'sub_b': 1}}
        selector = Selector(select_dict)
        self.assertEqual(selector.select_dict, select_dict)


class TestSelectorFactory(unittest.TestCase):

    def setUp(self):
        self.model_context = MagicMock(model.ModelContext)
        self.model_context.key_2_schema_column_map = {
            'a': SchemaColumn('a', {'format': 'x-long-text'}),
            'b': SchemaColumn('b', {'format': 'x-long-text'}),
            'c': SchemaColumn('c', {'format': 'x-long-text'}),
        }
        self.selector_factory = SelectorFactory(self.model_context)

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
        self.assertEqual(expected_result, selector.select_dict)

    def test_filter_non_zero(self):
        input_dict = {'a': 1, 'b': 0, 'c': 1, 'sub_table': {'sub_a': 0, 'sub_b': 1}}
        result = self.selector_factory.filter_non_zero(input_dict)
        expected_result = {'a': 1, 'c': 1, 'sub_table': {'sub_b': 1}}
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
