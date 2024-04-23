# Flask-Restful处理Controller

[flask-restful-quickstart](https://flask-restful.readthedocs.io/en/latest/quickstart.html#)

## 目标
通过本节学习可以快速开启一个httpserver demo。

## 示例
flask-restful和其他Http框架的使用方式大概一致。
我们以配置一个健康检查为例子
```python
from flask_restful import Resource, Api
from flask import Flask
APP = Flask(__name__)
API = Api(APP)

class HealthCheck(Resource):
    def get(self):
        print("HealthCheck")
        return {"success": True}

    def post(self):
        print("HealthCheck")
        return {"success": True}

API.add_resource(HealthCheck, '/HealthCheck')

if __name__ == '__main__':
    APP.run(port=8080, debug=True)
```

```sh
# start your python project
python3 your_project

# use get
curl http://127.0.0.1:8080/HealthCheck 

# use post
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8080/HealthCheck -d'{}'
```


## 注册多个Path
除此之外，我们可以给一个接口注册多个Path
```python
API.add_resource(HealthCheck,
    '/healthcheck',
    '/HealthCheck')
```
从demo示例可以看到， 这里类似go的httpserver的httpHandler的概念，写一个路由处理器，然后注册到对应路由位置。


## 同时我们也可以处理参数校验
```python
from flask_restful import reqparse, Resource, Api
from flask import Flask

class TestArgParse(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(dest='Required', required=True, help="Required is needed")
        parser.add_argument(dest='TestInt', type=int, required=True, help="TestInt must be an integer and required")
        parser.add_argument(dest='Optional', type=str, required=False, default="default",
                            help="Optional must be a string")
        args = parser.parse_args()
        print(f"args={args}")

APP = Flask(__name__)
API = Api(APP)
API.add_resource(TestArgParse, "/TestArgParse", "/testargparse")
if __name__ == '__main__':
    APP.run(port=8080, debug=True)
```

```sh

curl -X POST -H "Content-Type: application/json" "http://127.0.0.1:8080/TestArgParse" -d'{
}'

# expect
{
    "message": {
        "Required": "Required is needed"
    }
}

curl -X POST -H "Content-Type: application/json" "http://127.0.0.1:8080/TestArgParse" -d'{
  "Required":true,
  "TestInt":"str"
}'

# expect
{
    "message": {
        "TestInt": "TestInt must be an integer and required"
    }
}

curl -X POST -H "Content-Type: application/json" "http://127.0.0.1:8080/TestArgParse" -d'{
  "Required":true,
  "TestInt":10
}'

# expect
args={'Required': 'True', 'TestInt': 10, 'opt': 'default'}
```