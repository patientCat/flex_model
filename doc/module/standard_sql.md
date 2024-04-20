# 标准SQL

定义一套标准的SQL



## CRUD

### Example Schema
ModelUser

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {
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
        "id",
        "name",
        "age",
        "email"
    ]
}
```

---

Profile Schema
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {
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
            "properties": {},
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
        "id",
        "biography"
    ]
}

```

### 创建单条数据