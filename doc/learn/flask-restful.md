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
parser.add_argument('ModelName', type=str, required=True)
parser.add_argument('ProjectId', type=str, required=True)
parser.add_argument('Param', type=dict, required=True)
args = parser.parse_args()
```