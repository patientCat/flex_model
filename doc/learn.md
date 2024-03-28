# 学习Python3

## 定义全局Response
### BizResponse
根据Flask所需参数，定义status，message，header

其中message 即我们接口的返回体，一般返回Json类型格式
app/model/biz_response.py

### 定义装饰器
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
针对测试类TestResponse， 相当于增加一个dict_msg的方法。

### 鸭子类型
python本身是支持鸭子类型的。和go中鸭子类型一样。所以不需要像java中定义interface。
```python
class BizResponse:
    def __init__(self):
        self.status = 200
        self.message = None
        self.header = None
        pass

    def dict_msg(self):
        return self.message.dict_msg()

```
所以在Response中实现dict_msg，这里的目的就是将返回的response转为dict，交给Flask进行jsonify。
所以后续只需要在自定义的Response加上`@dict_response`装饰器即可。


## 使用单元测试
使用unittest进行单元测试
https://docs.python.org/zh-cn/3/library/unittest.html


使用go test 的类似写法，使用xxx_test 进行命名。

## 定义业务异常
```python
class BizException(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
```

个人倾向于使用string定义错误码。方便可读性。

定义全局异常处理
```python
@app.errorhandler(Exception)
def error_handler(e):
    """
    全局异常捕获
    """
    error = Error()
    if isinstance(e, BizException):
        error.message = e.message
        error.code = e.code
    else:
        error.message = f"error={e}"
        error.code = ErrorCode_InternalError
    response = BizResponse.fail(e)
    return jsonify(response.dict_msg()), response.status, response.header
```