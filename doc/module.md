# 模块介绍
## 模型上下文
### 1. 模型标识
模型标识映射为表名称

### 2. MetaInfo
MetaInfo为schema结构
存储模型字段信息

1. 插入和修改时候需要进行校验
2. 给前端提供表单信息，生成表单

### 3. 模型关联数据库上下文


## 数据库上下文
### 实现命名空间
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
依赖模型上下文, 根据模型上下文，生成对应的增删查改
自定义一套查询语法

### 实现query的查询翻译成mongo
```json
{
  "where": {
    "key": {
      "$eq": "abc"
    }
  }
}
```
### 实现select
```json
{
  "select": {
    "foo": 1,
    "bar": 1,
    "relate": {
      "select": {
        "name": 1,
        "age": 1
      }
    }
  }
}
```
### 实现orderBy
```json
{
  "orderBy": [{
    "column": 1
  },{
    "column": -1
  }]
}

```
### 实现limit，offset
```json
{
  "limit": 10,
  "offset": 1
}

```

## 实现创建，修改
### 实现创建，修改schema校验
### 实现必填字段校验

## 实现删除数据

## 实现模型元信息

模型的本质，就是利用字段，或者说元信息，对数据库字段赋予含义。或者说赋予业务功能。
此时，在使用时候，只需要考虑业务场景，不需要关系底层实现逻辑。

### 实现长短文本
### 实现时间戳
### 实现关联关系

### 实现根据schema，同步表字段