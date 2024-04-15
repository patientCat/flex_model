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
            "format": "x-short-text"
        },
        "name": {
            "type": "string",
            "format": "x-short-text"
        },
        "age": {
            "type": "number",
            "format": "x-number"
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
            "format": "x-short-text"
        },
        "biography": {
            "type": "string",
            "format": "x-short-text"
        },
        "userId": {
            "type": "string",
            "format": "x-short-text"
        },
        "user": {
            "type": "object",
            "properties": {},
            "format": "x-many-one",
            "x-relation": {
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