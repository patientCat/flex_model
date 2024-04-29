# 如何记录日志


## 记录日志

在生产系统中记录日志，一般需要定义成为json格式。方便filebeat进行上报到es中进行查询。

因此，对于我们的logger来说，只需要使用pythonjsonlogger即可。

[官方文档](https://pypi.org/project/python-json-logger/)


## 如何添加公共字段

对于我们的业务来说，通常需要记录一些公共字段，比如requestId值。这些是存在请求的header中的。而且每个请求唯一。

这里就需要使用到ThreadLocal了。

简单来说就是：
1. 将requestId以及其他业务字段存放在ThreadLocal中。
2. 然后在每次日志中进行输出。

简单封装了下ThreadLocal
[thread_local_utils](/app/common/thread_local_utils.py)

添加自定义字段
[示例](/app/common/bizlogger_test.py)

## 如何在Flask中进行集成
通过Flask自己定义的2个装饰器可以完成对出入口日志进行打印。同时将业务上下文属性设置进去

注意，每个请求都是一个线程。因此在after_request处，需要将所有的线程局部变量清空

```python
@APP.before_request
def before_request_func():
    BIZ_CONTEXT.set_attr(LogKey.action, request.path)
    BIZ_CONTEXT.set_attr(LogKey.request_id, request.headers.get("x-request-id", ""))
    request_body = request.get_json()
    BIZ_CONTEXT.set_attr(LogKey.mongo_project, request_body.get("ProjectId", ""))
    LOGGER.info(f"Handling request: {request.method} body:{request_body}")


@APP.after_request
def after_request_func(response):
    LOGGER.info(f"Handling response: {response.get_json()}")
    return response


```