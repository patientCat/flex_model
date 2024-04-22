# 如何高效组织代码
[github](https://github.com/patientCat/flex_model?tab=readme-ov-file)
## 组织代码

使用controller， service，domain的轻量DDD模式组织代码

这里算是一些个人经验所得。

controller： 负责校验参数，处理输入输出的返回。以及特殊错误的处理
service or api: 是业务逻辑的实现。负责组织domain。只负责业务，不关心底层逻辑。
domain: 每一个domain都是完善的业务模块。对外抽象底层逻辑。


单元测试：
在domain层需要最多的单元测试。保证每个domain的正常和异常情况处理。
在service层一般不需要单元测试，因为service层在业务开发中，应该是变化最多的地方。
在controller层不需要单元测试。都是使用的公共模块。且业务逻辑简单。

集成测试：
使用流水线进行集成测试。

### controller层处理
1. 参数校验，使用RequestParser

```python
from flask import Flask, request
from flask_requestparser import RequestParser

app = Flask(__name__)

# 初始化 RequestParser 对象
parser = RequestParser()

@app.route('/example')
def example():
    
    # 解析 GET 请求中的参数
    parser.add_argument('name', type=str, help='Name is required')
    parser.add_argument('age', type=int, help='Age is required')
   
    args = parser.parse_args()
  
    # 访问解析得到的参数值
    name = args.get('name')
    age = args.get('age')
    
    return f'Hello {name}! You are {age} years old.'
    
if __name__ == '__main__':
    app.run(debug=True)

```

2. 对每个请求的进行日志记录。方便排查bug。在java中可以用AOP，在go中可以注册mux，在python3中使用装饰器。

这里原理都是相同的，本质上就是代理模式。

这里需要2知识点。1个是线程局部变量。1个是如何记录日志。

```python
@APP.before_request
def before_request_func():
    BIZ_CONTEXT.set_attr(LogKey.action, request.path)
    BIZ_CONTEXT.set_attr(LogKey.request_id, request.headers.get("x-request-id", ""))
    request_body = request.get_json()
    BIZ_CONTEXT.set_attr(LogKey.project_id, request_body.get("ProjectId", ""))
    LOGGER.info(f"Handling request: {request.method} body:{request_body}")


@APP.after_request
def after_request_func(response):
    LOGGER.info(f"Handling response: {response.get_json()}")
    BIZ_CONTEXT.clear()
    return response


```


处理异常
处理异常我认为在编程中是非常重要的一个环节。它不仅决定了程序的稳定性，同时可以帮助程序员排查错误提供线索。要想不加班，异常处理十分重要。

对于服务来说需要全局统一处理异常。
```python
@APP.errorhandler(Exception)
def error_handler(e):
    """
    全局异常捕获
    """
    LOGGER.error("error={}", e)
    LOGGER.error("traceback={}", traceback.format_exc())
    if isinstance(e, BizException):
        message = e.message
        code = e.code
    else:
        message = f"error={e}"
        code = ErrorCode.InternalError.value
    response = BizResponse.fail(Error(message, code))
    return jsonify(response.dict_msg()), response.status, response.header



```
对于下面业务来说，只需要抛出异常即可。

### service层
传统的贫血模式代码，经常会导致service层写的非常重。包含大量凌乱的业务逻辑代码。

而目前比较流行的方式会增加一层domain层。将不同业务逻辑进行抽象，解耦。对于Service层来说，只需要对domain进行组织即可。
