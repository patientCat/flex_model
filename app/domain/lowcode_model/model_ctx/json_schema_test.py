import jsonschema
import unittest
import constant

example_schema = {
    "x-model-name": "quick_start",
    "x-namespace": "namespace1",
    "type": constant.TYPE_OBJECT,
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


class TestJsonSchema(unittest.TestCase):
    def test_max_items_schema(self):
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate([2, 3, 4], {"maxItems": 2})

    def test_example_schema(self):
        jsonschema.validate({"_id": "123"}, schema=example_schema)
        jsonschema.validate({"_id": "123", "short_text": "abc"}, schema=example_schema)
        jsonschema.validate({"_id": "123", "show_number": 123}, schema=example_schema)
        jsonschema.validate({"_id": "123", "json_column": {"a": 1}}, schema=example_schema)

    def test_err_example_schema(self):
        try:
            jsonschema.validate({"array_column": [{"name": 123}]}, schema=example_schema)
        except jsonschema.exceptions.ValidationError as e:
            print(e.cause)
            print(e.path)
            print(e.schema_path)
            pass
