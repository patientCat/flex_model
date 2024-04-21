# Readme
基于Http协议的数据库实现。

屏蔽底层数据库实现。可以自由将项目从mysql，mongo等进行切换。简化所有sql协议。使crud变得更加简单。

基于schema实现。可以通过schema快速生成表单。
## quickstart

1. 定义schema

数据模型通过json-schema定义通用的表结构。

ModelName: 定义模型的名字

ProjetId: 项目id

创建user模型
```curl
curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8080/CreateModel' \
-d '{
    "ModelName": "user",
    "ProjectId": "default",
    "ModelSchema": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "_id": {
                "type": "string",
                "format": "xShortText"
            },
            "name": {
                "type": "string",
                "format": "xShortText"
            },
            "age": {
                "type": "number",
                "format": "xNumber"
            },
            "email": {
                "type": "string",
                "format": "email"
            }
        },
        "required": [
            "name",
            "age"
        ]
    }
}'

```

创建profile模型
```curl
curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8080/CreateModel' \
-d '{
    "ModelName": "user",
    "ProjectId": "default",
    "ModelSchema": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "_id": {
                "type": "string",
                "format": "xShortText"
            },
            "biography": {
                "type": "string",
                "format": "xShortText"
            },
            "userId": {
                "type": "string",
                "format": "xShortText"
            },
            "user": {
                "type": "object",
                "properties": {

                },
                "format": "xManyToOne",
                "xRelation": {
                    "field": "userId",
                    "reference": {
                        "field": "id",
                        "model_name": "user"
                    }
                }
            }
        },
        "required": [
            "biography"
        ]
    }
}'
```

profile模型通过userId关联user模型


2. 对模型进行增删查改

创建一条数据
```curl
curl -X POST  -H "Content-Type: application/json" 'http://127.0.0.1:8080/CreateOne' \
-d '{
    "ModelName": "user",
    "ProjectId": "default",
    "Param": {
      "data":{
        "name": "luke",
        "age": 18
      }
    }
}'
```
```json
{
    "Response": {
        "Id": "662150a82ea4456eff41cb9e"
    }
}

```

查询一条数据
```json
curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8080/FindOne' \
-d '{
    "ModelName": "user",
    "ProjectId": "default",
    "Param": {
        "select": {
            "_id": 1,
            "name": 1
        },
        "limit": 10,
        "offset": 0,
        "where": {
            "name": "luke"
        }
    }
}'

{
    "Response": {
        "Record": {
            "_id": "662150a82ea4456eff41cb9e",
            "name": "luke"
        },
        "Total": null
    }
}
```

### 详细了解
[自动化测试用例](/autotest/base.py)

[](/接入协议)

## 项目讲解
低代码项目中的数据模型实现。

数据模型的意义就是对数据库表进行抽象。

### 数据模型表结构
对于普通开发者来说，使用数据库之前需要了解一些数据库特性，比如字段的类型，长度等概念。
对于不同数据库，比如mysql，mongo等，需要明白这些差异。

但是对于低码开发者来说，他们不需要关心这些细节。他们更关心的是我需要定义一个字段来存放email，存放图片，存放时间。
我不需要关心这些底层的实现细节。

#### 使用schema定义表结构
1. 可以利用schema本身具有的功能对写数据进行校验。
2. 前端可以通过schema进行表单的快速生成。

[快速了解schema](/doc/learn/learn_about_schema.md)

#### 定义查询协议
这里是广义的SQL（Structured Query Language，结构化查询语言）

通过定义一套通用的增，删，查，改协议，来简单操作我们的‘数据库’。

> 为什么不用Odata，要自研呢？ OData过于复杂。更加适合构建复杂系统。对于低码平台来说，往往构建的平台比较简单。
> 因此，协议最好简单，且容易使用。这里对标Prisma，实现了一套简单的通用协议。


### 实现自动化测试用例
目前的项目是一个微服务项目。不可避免的会依赖一些其诸如数据库。因此我们的项目除了单元测试以外，还需要进行集成测试。

所以这里提供最基础的自动测试用例。

/autotest

后续可以接入流水线，作为部署后的自动化测试。


## Python3工程学习

[Json和python字典深入学习](/doc/learn/json_and_dict.md)

[如何进行统一全局Response结构和处理全局业务异常](/doc/learn/global_error_handle.md)

[使用flask-restful进行controller处理](/doc/learn/flask-restful.md)

[使用sqlalchemy进行数据库处理](/doc/learn/learn_repo.md)

[处理日志](/doc/learn/learn_logger.md)
