# 模块介绍

## 数据库上下文

1. 设计命名空间：逻辑区分，默认使用default作为命名空间
2. 表名称

example
```shell
namespace: default
table_name: user
collection_name: default_user
```

### 单元测试
使用unittest进行单元测试
https://docs.python.org/zh-cn/3/library/unittest.html



## 实现查询DSL
自定义一套查询语法


## 实现模型元信息

模型的本质，就是利用字段，或者说元信息，对数据库字段赋予含义。或者说赋予业务功能。
此时，在使用时候，只需要考虑业务场景，不需要关系底层实现逻辑。