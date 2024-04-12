import unittest

from app.common.error import BizException
from app.domain.lowcode_model.model_ctx import field
from model import ModelContext, MetadataContext


class TestMetadataContext(unittest.TestCase):

    def setUp(self):
        self.json_schema = {
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
        self.metadata_context = MetadataContext(self.json_schema)

    def test_get_column_list_from_schema(self):
        column_list = self.metadata_context.get_column_list_from_schema(self.json_schema)
        self.assertIsInstance(column_list, list)
        self.assertEqual(len(column_list), 2)
        self.assertIsInstance(column_list[0], field.SchemaColumn)
        self.assertIsInstance(column_list[1], field.SchemaColumn)

    def test_column_list(self):
        column_list = self.metadata_context.column_list
        self.assertIsInstance(column_list, list)
        self.assertEqual(len(column_list), 2)
        self.assertIsInstance(column_list[0], field.SchemaColumn)
        self.assertIsInstance(column_list[1], field.SchemaColumn)

    def test_validate_on_create(self):
        param = {"data": {"name": "John", "age": 30}}
        self.metadata_context.validate_on_create(param)  # 应该不抛出异常

        param = {"data": {"name": "John", "age": "30"}}
        with self.assertRaises(BizException):
            self.metadata_context.validate_on_create(param)

    def test_validate_on_create_many(self):
        param = {"data": [{"name": "John", "age": 30}, {"name": "Jane", "age": 28}]}
        self.metadata_context.validate_on_create_many(param)  # 应该不抛出异常

        param = {"data": [{"name": "John", "age": 30}, {"name": "Jane", "age": "28"}]}
        with self.assertRaises(BizException):
            self.metadata_context.validate_on_create_many(param)

    def test_validate_on_update(self):
        param = {"data": {"name": "John", "age": 30}}
        self.metadata_context.validate_on_update(param)  # 应该不抛出异常

        param = {"data": {"name": "John", "age": "30"}}
        with self.assertRaises(BizException):
            self.metadata_context.validate_on_update(param)


class TestModelClass(unittest.TestCase):

    def setUp(self):
        self.schema = example_schema = {
            "x-model-name": "quick_start",
            "x-namespace": "namespace1",
            "x-database-name": "test",
            "type": "object",
            "properties": {
                "_id": {
                    "x-name": "_id",
                    "x-title": "主键",
                    "type": "string",
                },
                "short_text": {
                    "format": "x-short-text",
                    "x-name": "short_text",
                    "x-title": "短文本",
                    "type": "string",
                },
                "show_number": {
                    "format": "x-number",
                    "x-name": "show_number",
                    "x-title": "数字",
                    "type": "number",
                },
                "json_column": {
                    "type": "object",
                },
                "array_column": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                            }
                        }
                    }
                }
            }
        }

        example_model = ModelContext.create_from_schema(example_schema)
        self.example_model = example_model

    def test_schema_column_list(self):
        expected_result = ["_id", "short_text", "show_number", "json_column", "array_column"]
        actual_result = [col.id for col in list(self.example_model.schema_column_list())]
        self.assertEqual(actual_result, expected_result)

    def test_schema_field(self):
        print(self.example_model.metadata_ctx.__dict__)

    def test_schema_name(self):
        self.assertEqual(self.example_model.schema_column("_id").id, "_id")
        self.assertEqual(self.example_model.schema_column("short_text").id, "short_text")


if __name__ == '__main__':
    unittest.main()
