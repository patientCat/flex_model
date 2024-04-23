# 全局统一参数和异常处理
[github](https://github.com/patientCat/flex_model?tab=readme-ov-file)
## 前言
主要谈在Python中，
1. 如何进行统一的Request，Response处理。
2. 如何进行全局异常处理。

在实际业务中，我们往往需要定义统一的Request，Response处理。
不仅仅方便其他方对接，同时也方便我们的业务处理。

## 处理Request
对于Controller来说，需要将用户请求，从body，path中解出来。然后解析成Request交给Service


## 处理Response
对于Response来说
1. 正确时要按照统一的格式返回出参。
2. 错误时要按照统一的格式返回错误。


### BizResponse
根据Flask所需参数，定义status，message，header

返回的header，我们很少关心

返回的status，按照业务返回即可。一般成功返回200。错误根据服务端错误和客户端错误自行确定，项目初期，可以区分下即可。

返回的message 即我们接口的返回体，一般返回Json类型格式
这里是我们重点关心的地方，要保证有统一的返回结构体。

我们的BizResponse需要封装一下，这样才能统一处理。

我们预期的格式是
```
# 正确类型
{
  "RequestId":"xxx",
  "Response":{
    "BizResp":{
      "Test":true
    }
  }
}
# 错误类型
{
  "RequestId":"xxx",
  "Response":{
    "Error":{
      "Code":"InvalidParameter",
      "Message":"Param should be string"
    }
  }
}
```
这里涉及到一点线程局部变量的问题。后续章节会介绍。
```python
class BizResponse:
    def __init__(self):
        self.status = 200
        self.message = None
        self.header = None
        pass

    @staticmethod
    def success(response) -> "BizResponse":
        resmsg = BizResponse()
        resmsg.message = response
        resmsg.status = 200
        return resmsg

    @staticmethod
    def fail(error: Error) -> "BizResponse":
        resmsg = BizResponse()
        resmsg.message = error
        resmsg.status = 400
        return resmsg

    def dict_msg(self):
        return {
            "RequestId": BIZ_CONTEXT.get_attr(LogKey.request_id),
            "Response": self.message.dict_msg()
        }



```
代码详细请看
[github](https://github.com/patientCat/flex_model?tab=readme-ov-file)
app/model/biz_response.py

#### 思路
我们定义统一的biz_response来处理Flask的所有返回参数。
其中，对于参数message 要求必须实现dict_msg()这个函数

dict_msg()函数负责将出参映射成为希望看到的样子。

因为在python中的命名规范是小写下划线。所以为了方便转化，我们要将所有的VO对象实现这个方法。

这里有如下几种方法。

1. 通过装饰器加魔术方法实现。但是这样实现没办法控制字段的转化。比如abc -> Abc。
2. 每个VO手动实现。

#### 定义装饰器
装饰器的感觉和java的注解类似，实现 dict_response
```python
def dict_response(cls):
    def dict_msg(cls):
        return {key: value for key, value in cls.__dict__.items()}

    cls.dict_msg = dict_msg
    return cls

@dataclass
@dict_response
class TestResponse:
    name: str
    age: int
```
通过装饰器dict_response, 为TestResponse增加一个dict_msg的方法。

上述的方法也可以手动实现
```python
class TestResponse:
    name: str
    age: int
    def dict_msg(cls):
      return {"name":cls.name, "age":cls.age}

```

### 额外学习：鸭子类型
python没有Java中的interface的概念。

python本身是支持鸭子类型的。和go中鸭子类型一样。所以不需要像java中定义interface。
```python
class Animal:
    def bark(cls):
        print("im a animal")

class Dog:
    def bark(cls):
        print("wang wang")

animal : Animal = Dog()
animal.bark() # wang wang
```

#### 示例展示
```python3
class TestBizResponse(unittest.TestCase):
    def setUp(self) -> None:
        BIZ_CONTEXT.set_attr(LogKey.request_id, "request_id")

    def test_success(self):
        message = test_response.TestResponse(name="John Doe", age=10)
        res = BizResponse.success(message)
        self.assertEqual(res.status, 200)
        self.assertEqual(res.message, message)

    def test_fail(self):
        error = Error("Error message", ErrorCode.InvalidParameter.value)
        res = BizResponse.fail(error)
        self.assertEqual(res.status, 400)
        self.assertEqual(res.message, error)
        print(res.dict_msg())
        self.assertTrue('Response' in res.dict_msg())

```
所以在BizResponse中，直接使用message的dict_msg()方法，不用关心具体的类型。
同时这也意味着我们所有的返回Response，都应该实现这个方法。
[详细示例请看](/app/common/biz_response_test.py)

到此为止，我们就能完全统一我们的返回结构体。


## 使用单元测试
使用unittest进行单元测试
https://docs.python.org/zh-cn/3/library/unittest.html


使用go test 的类似写法，使用xxx_test 进行命名。

## 定义业务异常
代码详细请查看 app/common/error.py
```python
#app/common/error.py
class ErrorCode(Enum):
    InternalError = "InternalError"
    InvalidParameter = "InvalidParameter"


class BizException(Exception):
    def __init__(cls, code: ErrorCode, message: str):
        cls.code = code
        cls.message = message


class Error:
    def __init__(cls, msg: str, code: str):
        cls.message = msg
        cls.code = code

    def dict_msg(cls):
        return {
            "Error": {
                "Message": cls.message,
                "Code": cls.code
            }
        }

```
定义业务异常的目的也是为了更好地通过错误代码错误，并判断错误原因。

个人倾向于使用string定义错误码。方便可读性。

定义全局异常处理
```python
@app.errorhandler(Exception)
def error_handler(e):
    """
    全局异常捕获
    """
    logger.error("error=%s", e)
    logger.error("traceback=%s", traceback.format_exc())
    if isinstance(e, BizException):
        message = e.message
        code = e.code.value
    else:
        message = f"error={e}"
        code = ErrorCode.InternalError.value
    response = BizResponse.fail(Error(message, code))
    return jsonify(response.dict_msg()), response.status, response.header


```