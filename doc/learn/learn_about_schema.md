# 学习schema

json-schema主要用来校验json数据。
[中文文档](https://json-schema.apifox.cn/)
[python3官方文档](https://python-jsonschema.readthedocs.io/en/stable/)

以下是ai的回答


> 常见的使用场景
> 1. API 数据交互: 在 Web API 开发过程中，通过 JSON Schema 来统一和规范接口请求及响应的数据格式可以降低开发和维护成本和提高互操作性。
> 2. 前后端数据传输: 对于前端和后端的通信而言，采用 JSON Schema 能够保证数据的一致性及准确性从而提高应用程序的性能和质量。
> 3. 数据存储: 当您将 JSON 数据持久化至数据库或其它存储系统前，利用 JSON Schema 进行预处理和验证有助于避免无效或不正确的数据存入造成的问题和数据混乱现象的发生。


## 常用属性
json-schema的校验属性很多。这里只介绍常见的几个。

### number
测试最大最小值
```python
class NumberOfSchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.number_schema = {
            "type": "object",
            "properties": {
                "price": {"type": "number", "minimum": 5},
                "priceHigh": {"type": "number", "maximum": 10},
            },
        }

    def test_number_minimum_schema(self):
        try:
            jsonschema.validate(instance={"price": 3}, schema=self.number_schema)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            self.assertEqual(e.validator, "minimum")

    def test_number_maximum_schema(self):
        try:
            jsonschema.validate(instance={"priceHigh": 13}, schema=self.number_schema)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            self.assertEqual(e.validator, "maximum")
```

### string
校验长度

```python
class StringOfSchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.number_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 5},
                "nameLong": {"type": "string", "maxLength": 10},
            },
        }

    def test_minLength_schema(self):
        try:
            jsonschema.validate(instance={"name": "abc"}, schema=self.number_schema)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            self.assertEqual(e.validator, "minLength")

    def test_maxLength_schema(self):
        try:
            jsonschema.validate(instance={"nameLong": "acdefghijklmnopq"}, schema=self.number_schema)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            self.assertEqual(e.validator, "maxLength")
```

### 校验必填字段

测试必填字段
```python

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


```

### 校验特殊格式

测试format，测试ipv4
```python

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

    def test_wrong_format(self):
        try:
            jsonschema.validate(instance={"ipv4": "012", "age": 10},
                                schema=self.schema, format_checker=self.format_checker)
        except jsonschema.exceptions.ValidationError as e:
            print(e.message)
            print(e.validator)
            self.assertEqual(e.validator, "format")


```