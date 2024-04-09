# 全局Response返回和异常处理

## 前言
主要谈在Python中，
1. 如何进行统一Response处理。
2. 如何进行全局异常处理。

## 定义全局Response
### BizResponse
根据Flask所需参数，定义status，message，header

返回的header，我们很少关心

返回的status，按照业务返回即可。一般成功返回200。错误根据服务端错误和客户端错误自行确定，项目初期，可以区分下即可。

返回的message 即我们接口的返回体，一般返回Json类型格式
这里是我们重点关心的地方，要保证有统一的返回结构体。

代码详细请看
app/model/biz_response.py

#### 思路
我们定义统一的biz_response来处理Flask的所有返回参数。
其中，对于参数message 要求必须实现dict_msg()这个函数

dict_msg()函数负责将出参映射成为希望看到的样子

#### 定义装饰器
装饰器的感觉和java的注解类似，实现 dict_response
```python
def dict_response(cls):
    def dict_msg(self):
        return {key: value for key, value in self.__dict__.items()}

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
    def dict_msg(self):
      return {"name":self.name, "age":self.age}

```

### 额外学习：鸭子类型
python没有Java中的interface的概念。

python本身是支持鸭子类型的。和go中鸭子类型一样。所以不需要像java中定义interface。
```python
class Animal:
    def bark(self):
        print("im a animal")

class Dog:
    def bark(self):
        print("wang wang")

animal : Animal = Dog()
animal.bark() # wang wang
```

```python3
#biz_response.py
class BizResponse:
    def dict_msg(self):
        return {
            "Response": self.message.dict_msg()
        }

@dataclass
class TestResponse:
    id: str
    
    def dict_msg(self):
        # 手动改为大写开头的格式
        return {
            "Id": self.id,
        }

```
所以在BizResponse中，直接使用message的dict_msg()方法，不用关心具体的类型。
同时这也意味着我们所有的返回Response，都应该实现这个方法。
[详细示例请看](/app/model/biz_response_test.py)

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
    def __init__(self, code: ErrorCode, message: str):
        self.code = code
        self.message = message


class Error:
    def __init__(self, msg: str, code: str):
        self.message = msg
        self.code = code

    def dict_msg(self):
        return {
            "Error": {
                "Message": self.message,
                "Code": self.code
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