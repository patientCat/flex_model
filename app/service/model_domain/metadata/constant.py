# 长度不超过256，用来存放一些标识，可以建立索引
FORMAT_SHORT_TEXT = "x-short-text"
# 存放长文本数据，不可以建立索引
FORMAT_LONG_TEXT = "x-long-text"
# 普通数字
FORMAT_NUMBER = "x-number"
# 自定义json字段, 自己负责校验
FORMAT_JSON = "x-json"
# 多对一关联关系
FORMAT_MANY_TO_ONE = "x-many-to-one"
# 一对多关联关系
FORMAT_ONE_TO_MANY = "x-one-to-many"
# 多对多关联关系
FORMAT_MANY_TO_MANY = "x-many-to-many"


SCHEMA_KEY_FORMAT = "format"
SCHEMA_KEY_TYPE = "type"
