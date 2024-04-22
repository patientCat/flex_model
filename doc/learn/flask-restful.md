# Flask-Restful处理Controller

[flask-restful-quickstart](https://flask-restful.readthedocs.io/en/latest/quickstart.html#)


使用flask-restful主要目的是解决如下问题

## 注册多个路由
```python
api.add_resource(HelloWorld,
    '/',
    '/hello')
```
从demo示例可以看到， 这里类似go的httpserver的httpHandler的概念，写一个路由处理器，然后注册到对应路由位置。


## 处理参数校验
```python
parser = reqparse.RequestParser()
parser.add_argument('TestStr', type=str, required=True)
parser.add_argument('TestInt', type=int, required=True)
parser.add_argument('Param', type=dict, required=True)
args = parser.parse_args()
```

## 示例
我们以配置一个健康检查为例子
```python
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