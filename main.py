# save this as main.py
from types import SimpleNamespace

from flask import Flask, jsonify, request
from app.model.biz_response import BizResponse, Error
from app.model.param.test_response import TestResponse
from app.common.error import BizException
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


runtime_service = RuntimeService()


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
    json_body = SimpleNamespace(**body)
    req = create.CreateOneRequest(json_body.model_name, json_body.param)
    response = runtime_service.createOne(req)
    success = BizResponse.success(response)
    return jsonify(success.dict_msg()), success.status, success.header


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


if __name__ == '__main__':
    app.run(port=8080, debug=True)
