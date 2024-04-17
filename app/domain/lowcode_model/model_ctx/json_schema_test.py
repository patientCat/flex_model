import json

import jsonschema
import unittest

from jsonschema.validators import Draft202012Validator

from app.domain.lowcode_model.model_ctx.json_schema import JsonSchemaChecker, get_key_from_json_path, _get_many_schema


class TestJsonSchemaChecker(unittest.TestCase):

    def setUp(self):
        self.json_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "city": {"type": "string"}
            },
            "required": ["name", "age"]
        }
        self.checker = JsonSchemaChecker(self.json_schema, fail_first=False)

    def test_get_many_json_schema(self):
        rtn = _get_many_schema(self.json_schema)
        print(json.dumps(rtn))

    def test_get_key_from_json_path(self):
        rtn = get_key_from_json_path("$.abc")
        print(rtn)
        self.assertEqual(rtn, "abc")

    def test_validate_on_create(self):
        valid_data = {"name": "John", "age": 30, "city": "New York"}
        valid_result = self.checker.validate_on_create(valid_data)
        self.assertTrue(valid_result.is_valid)

        invalid_data = {"name": "John", "city": 123}
        valid_result = self.checker.validate_on_create(invalid_data)
        self.assertTrue(not valid_result.is_valid)
        print(f"{valid_result.error_message}")

    def test_validate_on_create_many(self):
        valid_data = [{"name": "John", "age": 30, "city": "New York"}]
        valid_result = self.checker.validate_on_create_many(valid_data)
        print(valid_result)
        self.assertTrue(valid_result.is_valid)

        invalid_data = [{"name": "John", "city": 123}]
        valid_result = self.checker.validate_on_create_many(invalid_data)
        print(valid_result)
        self.assertTrue(not valid_result.is_valid)
        print(f"{valid_result.error_message}")

    def test_validate_on_update(self):
        valid_data = {"name": "John", "age": 30, "city": "New York"}
        valid_result = self.checker.validate_on_update(valid_data)
        self.assertTrue(valid_result.is_valid)

        valid_data = {"city": "New York"}
        valid_result = self.checker.validate_on_update(valid_data)
        self.assertTrue(valid_result.is_valid)

        invalid_data = {"name": "John", "age": "30"}
        valid_result = self.checker.validate_on_update(invalid_data)
        self.assertTrue(not valid_result.is_valid)
        print(f"{valid_result.error_message}")


class TestJsonSchema(unittest.TestCase):
    def setUp(self):
        self.schema = {
            "x-model-name": "quick_start",
            "x-namespace": "namespace1",
            "type": "type",
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

    def test_max_items_schema(self):
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate([2, 3, 4], {"maxItems": 2})

    def test_example_schema(self):
        jsonschema.validate({"_id": "123"}, schema=self.schema)
        jsonschema.validate({"_id": "123", "short_text": "abc"}, schema=self.schema)
        jsonschema.validate({"_id": "123", "show_number": 123}, schema=self.schema)
        jsonschema.validate({"_id": "123", "json_column": {"a": 1}}, schema=self.schema)

    def test_err_example_schema(self):
        try:
            jsonschema.validate({"array_column": [{"name": 123}]}, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            print(e.cause)
            print(e.path)
            print(e.schema_path)
            pass


class NumberOfSchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = {
            "type": "object",
            "properties": {
                "price": {"type": "number", "minimum": 5},
                "priceHigh": {"type": "number", "maximum": 10},
            },
        }

    def test_minimum_schema(self):
        try:
            jsonschema.validate(instance={"price": 3}, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            self.assertEqual(e.validator, "minimum")

    def test_maximum_schema(self):
        try:
            jsonschema.validate(instance={"priceHigh": 13}, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            self.assertEqual(e.validator, "maximum")


class StringOfSchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 5},
                "nameLong": {"type": "string", "maxLength": 10},
            },
        }

    def test_minLength_schema(self):
        try:
            jsonschema.validate(instance={"name": "abc"}, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            self.assertEqual(e.validator, "minLength")

    def test_maxLength_schema(self):
        try:
            jsonschema.validate(instance={"nameLong": "acdefghijklmnopq"}, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            self.assertEqual(e.validator, "maxLength")


class RequiredOfSchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"},
            },
            "required": ["name", "age"]
        }

    def test_ok(self):
        try:
            jsonschema.validate(instance={"name": "foo", "age": 10}, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            self.assertTrue(True is False)

    def test_lack_age(self):
        try:
            jsonschema.validate(instance={"name": "foo"}, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            self.assertEqual(e.validator, "required")


class FormatOfSchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = {
            "type": "object",
            "properties": {
                "ipv4": {"type": "string", "format": "ipv4"},
                "age": {"type": "number"},
            },
        }

        self.format_checker = Draft202012Validator.FORMAT_CHECKER

    def test_ok(self):
        try:
            jsonschema.validate(instance={"ipv4": "127.0.0.1", "age": 10},
                                schema=self.schema, format_checker=self.format_checker)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            self.assertTrue(True is False)

    def test_example(self):
        v = Draft202012Validator(self.schema)
        v.format_checker = self.format_checker
        error_list = v.iter_errors(instance={"ipv4": "127.0.0.1", "age": 123})
        print("error_list=", error_list is None)
        for e in sorted(error_list, key=str):
            print(e.message)
            print(e.validator)
            print(e.relative_path)
            print(e.json_path)
            print(e.cause)
            print(e.instance)

    def test_wrong_format(self):
        try:
            jsonschema.validate(instance={"ipv4": "012", "age": 123},
                                schema=self.schema, format_checker=self.format_checker)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            print(e.relative_path)
            print(e.json_path)
            print(e.cause)
            print(e.instance)
            self.assertEqual(e.validator, "format")


class ArrayOfSchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "ipv4": {"type": "string", "format": "ipv4"},
                    "age": {"type": "number"},
                },
                "required": ["ipv4", "age"]
            },
        }

        self.format_checker = Draft202012Validator.FORMAT_CHECKER

    def test_ok(self):
        try:
            jsonschema.validate(instance=[{"ipv4": "127.0.0.1", "age": 10}],
                                schema=self.schema, format_checker=self.format_checker)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            self.assertTrue(True is False)

    def test_wrong_format(self):
        try:
            jsonschema.validate(instance=[{"ipv4": "127.0.0.1"}],
                                schema=self.schema, format_checker=self.format_checker)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            print(e.relative_path)
            print(e.json_path)
            print(e.cause)
            print(e.instance)
            # self.assertEqual(e.validator, "type")
