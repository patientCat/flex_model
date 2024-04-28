# 定义数据模型模块

定义低代码中的数据模型

## 数据模型

数据模型的含义是对持久化对象的抽象。并应用于业务。同时还具有对数据的约束作用。

同时根据数据模型，又可以快速生成表单。

业界标准的做法就是使用json-schema来做。

什么是[json-schema](https://json-schema.apifox.cn/)

### 模型标识
模型标识即表名

### namespace
逻辑命名空间，用来将模型逻辑分组。

### schema元信息
#### 校验生成的schema是否合法

json-schema在管理流进行生成，在数据流会验证数据。那么就要保证json-schema的合法性。

因为要支持不同的字段，对不同字段的格式进行验证。很自然就想到了工厂模式 + 策略模式。

```python
from abc import abstractmethod

from app.domain.lowcode_model.model_ctx.column import SchemaColumn, ColumnType, ColumnFormat


class ColumnValidator:
    @abstractmethod
    def validate(self, column: SchemaColumn) -> (bool, str):
        pass


class ShortTextValidator(ColumnValidator):
    def validate(self, column: SchemaColumn) -> (bool, str):
        if column.type != ColumnType.STRING:
            return False, f"{column.format} must be a string type"
        json_val = column.json_val
        max_length: int = json_val.get("maxLength")
        if max_length is None:
            return False, f"{column.format} maxLength must be defined"
        max_limit = 256
        if max_length > max_limit:
            return False, f"{column.format} maxLength must be <= {max_limit}"
        return True, ""


class LongTextValidator(ColumnValidator):
    def validate(self, column: SchemaColumn):
        if column.type != ColumnType.STRING:
            return False, f"{column.format} must be a string type"
        json_val = column.json_val
        max_length: int = json_val.get("maxLength")
        if max_length is None:
            return False, f"{column.format} maxLength must be defined"
        max_limit = 64 * 1024
        if max_length > max_limit:
            return False, f"{column.format} maxLength must be <= {max_limit}"
        return True, ""


class ColumnValidatorFactory:
    def __init__(self):
        self.__validator_dict = {
            ColumnFormat.SHORT_TEXT: ShortTextValidator(),
            ColumnFormat.LONG_TEXT: LongTextValidator(),
        }

    def create_validator(self, column_format: ColumnFormat):
        return self.__validator_dict.get(column_format)

```

### 关联工程id
每个工程存有对应的数据库信息。

## 数据模型的相关接口

1. 创建数据模型
2. 删除数据模型
3. 查询数据模型

对数据模型的修改分为对列的操作。

1. 增加列
2. 修改列
3. 删除列


## 完成自动化测试
[自动化测试](/autotest/manage_auto_test.py)