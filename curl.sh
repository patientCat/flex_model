localhost:8080

### Send POST request with json body
POST https://localhost:8080/findOne



### Send POST request with json body
curl -X POST 'http://127.0.0.1:8080/createOne' \
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
