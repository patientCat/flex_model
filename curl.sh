localhost:8080

### Send POST request with json body
### FindOne
curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8080/FindOne' \
-d '{
    "ModelName": "luke_test",
    "ProjectId": "default",
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

### FindOne with withCount
curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8080/FindOne' \
-d '{
    "ModelName": "luke_test",
    "ProjectId": "default",
    "Param": {
        "select": {
            "id": 1,
            "name": 1
        },
        "limit": 10,
        "offset": 0,
        "where": {
            "name": "foo"
        },
        "withCount":true
    }
}'
### FindMany
curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8080/FindMany' \
-d '{
    "ModelName": "luke_test",
    "ProjectId": "default",
    "Param": {
        "select": {
            "id": 1,
            "name": 1
        },
        "limit": 3,
        "offset": 0,
        "where": {
        }
    }
}'

### FindMany with withCount
curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8080/FindMany' \
-d '{
    "ModelName": "luke_test",
    "ProjectId": "default",
    "Param": {
        "select": {
            "id": 1,
            "name": 1
        },
        "limit": 3,
        "offset": 0,
        "where": {
            "name": "foo"
        },
        "withCount":true
    }
}'

### CreateOne
curl -X POST  -H "Content-Type: application/json" 'http://127.0.0.1:8080/CreateOne' \
-d '{
    "ModelName": "luke_test",
    "ProjectId": "default",
    "Param": {
      "data":{
        "name": "foo",
        "age": "1"
      }
    }
}'

### CreateMany
curl -X POST  -H "Content-Type: application/json" 'http://127.0.0.1:8080/CreateMany' \
-d '{
    "ModelName": "luke_test",
    "ProjectId": "default",
    "Param": {
      "data":[{
        "name": "foo",
        "age": 1
      },
      {
        "name": "bar",
        "age": "2"
      }]
    }
}'

### UpdateOne
curl -X POST  -H "Content-Type: application/json" 'http://127.0.0.1:8080/UpdateOne' \
-d '{
    "ModelName": "luke_test",
    "ProjectId": "default",
    "Param": {
      "where": {
        "name": "123"
      },
      "data":{
        "name": "foo",
        "age": 1
      }
    }
}'

### UpdateMany
curl -X POST  -H "Content-Type: application/json" 'http://127.0.0.1:8080/UpdateMany' \
-d '{
    "ModelName": "luke_test",
    "ProjectId": "default",
    "Param": {
      "where": {
        "name": "123"
      },
      "data":{
        "name": "foo",
        "age": 1
      }
    }
}'

### DeleteOne
curl -X POST  -H "Content-Type: application/json" 'http://127.0.0.1:8080/DeleteOne' \
-d '{
    "ModelName": "luke_test",
    "ProjectId": "default",
    "Param": {
      "where": {
        "name": "foo"
      }
    }
}'

### DeleteOne check unique
curl -X POST  -H "Content-Type: application/json" 'http://127.0.0.1:8080/DeleteOne' \
-d '{
    "ModelName": "luke_test",
    "ProjectId": "default",
    "Param": {
      "where": {
        "name": "foo"
      },
      "unique":true
    }
}'

### DeleteMany
curl -X POST  -H "Content-Type: application/json" 'http://127.0.0.1:8080/DeleteMany' \
-d '{
    "ModelName": "luke_test",
    "ProjectId": "default",
    "Param": {
      "where": {
        "name": "123"
      }
    }
}'