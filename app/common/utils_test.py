import unittest
from dataclasses import dataclass

from utils import serialize_instance, toJSON  # 请将your_module替换为实际的模块名


class TestSerializeInstance(unittest.TestCase):
    def test_serialize_instance_with_to_json(self):
        class TestClass:
            def __init__(self):
                self.value = 42

            def to_json(self):
                return {"value": self.value}

        obj = TestClass()
        result = serialize_instance(obj)
        self.assertEqual(result, {"value": 42})

    def test_serialize_instance_dataclass(self):
        @dataclass
        class TestClass:
            value: int

        obj = TestClass(42)
        result = serialize_instance(obj)
        self.assertEqual(result, {"value": 42})

    def test_serialize_instance_with_dict(self):
        class TestClass:
            def __init__(self):
                self.value = 42

        obj = TestClass()
        result = serialize_instance(obj)
        self.assertEqual(result, {"value": 42})


class TestToJSON(unittest.TestCase):
    def test_toJSON_with_none(self):
        result = toJSON(None)
        self.assertIsNone(result)

    def test_toJSON_with_serializer(self):
        class TestClass:
            def __init__(self):
                self.value = 42

        def custom_serializer(obj):
            return {"value": obj.value}

        obj = TestClass()
        result = toJSON(obj, serializer=custom_serializer)
        self.assertEqual(result, '{"value": 42}')

    def test_toJSON_without_serializer(self):
        class TestClass:
            def __init__(self):
                self.value = 42

        obj = TestClass()
        result = toJSON(obj)
        self.assertEqual(result, '{"value": 42}')


if __name__ == "__main__":
    unittest.main()
