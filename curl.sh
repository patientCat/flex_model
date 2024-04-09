localhost:8080

### Send POST request with json body
### FindOne
curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8080/FindOne' \
-d '{
    "ModelName": "luke_test",
    "TenantId": "tnt_test",
    "Param": {
        "select": {
            "id": 1,
            "name": 1
        },
        "limit": 10,
        "offset": 0,
        "where": {
            "name": "foo"
        }
    }
}'
### FindMany
curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8080/FindMany' \
-d '{
    "ModelName": "luke_test",
    "TenantId": "tnt_test",
    "Param": {
        "select": {
            "id": 1,
            "name": 1
        },
        "limit": 10,
        "offset": 0,
        "where": {
            "name": "foo"
        }
    }
}'


### CreateOne
curl -X POST  -H "Content-Type: application/json" 'http://127.0.0.1:8080/CreateOne' \
-d '{
    "ModelName": "luke_test",
    "TenantId": "tnt_test",
    "Param": {
      "data":{
        "name": "foo",
        "age": 1
      }
    }
}'

### CreateMany
curl -X POST  -H "Content-Type: application/json" 'http://127.0.0.1:8080/CreateMany' \
-d '{
    "ModelName": "luke_test",
    "TenantId": "tnt_test",
    "Param": {
      "data":[{
        "name": "foo",
        "age": 1
      },
      {
        "name": "bar",
        "age": 2
      }]
    }
}'
