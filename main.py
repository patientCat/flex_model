# save this as main.py
from types import SimpleNamespace

from flask import Flask, jsonify, request

from app.api.context import ContextHolder
from app.common.utils import CustomNamespace
from app.model.biz_response import BizResponse, Error
from app.model.param.test_response import TestResponse
from app.common.error import BizException, ErrorCode
from app.common.errorcode import *
from app.api.runtime import RuntimeService
from app.model.param import find, create

app = Flask(__name__)


@app.route("/")
def hello():
    res = TestResponse("luke", 12)
    print(res)
    success = BizResponse.success(res)
    return jsonify(success.dict_msg()), success.status, success.header


context_holder = ContextHolder()
runtime_service = RuntimeService(context=context_holder)


@app.post("/findOne")
def findOne():
    body = request.get_json(force=True)
    json_body = SimpleNamespace(**body)
    req = find.FindOneRequest(json_body.model_name, json_body.param)
    response = runtime_service.findOne(req)
    success = BizResponse.success(response)
    return jsonify(success.dict_msg()), success.status, success.header


@app.post("/findMany")
def findMany():
    return "findMany"


@app.post("/createOne")
def createOne():
    body = request.get_json(force=True)
    print(f'body={body}')
    req = create.CreateOneRequest(**body)
    response = runtime_service.createOne(req)
    success = BizResponse.success(response)
    return jsonify(success.dict_msg()), success.status, success.header


@app.errorhandler(Exception)
def error_handler(e):
    """
    全局异常捕获
    """
    if isinstance(e, BizException):
        message = e.message
        code = e.code.value
    else:
        message = f"error={e}"
        code = ErrorCode.InternalError.value
    response = BizResponse.fail(Error(message, code))
    return jsonify(response.dict_msg()), response.status, response.header


if __name__ == '__main__':
    app.run(port=8080, debug=True)
