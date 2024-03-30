import unittest

from model import ModelContext

example_schema = {
    "x-model-name": "quick_start",
    "x-namespace": "namespace1",
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


class TestModelClass(unittest.TestCase):

    def setUp(self):
        example_model = ModelContext.create_from_schema(example_schema)
        self.example_model = example_model

    def test_schema_column_list(self):
        expected_result = ["_id", "short_text", "show_number", "json_column", "array_column"]
        actual_result = [col.name for col in list(self.example_model.schema_column_list())]
        self.assertEqual(actual_result, expected_result)

    def test_schema_name(self):
        self.assertEqual(self.example_model.schema_column("_id").name, "_id")
        self.assertEqual(self.example_model.schema_column("short_text").name, "short_text")


if __name__ == '__main__':
    unittest.main()
