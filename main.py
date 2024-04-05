# save this as main.py
import logging
import traceback

from flask import Flask, jsonify, request

from app.api.context import ContextHolder
from app.api.runtime import RuntimeService
from app.common.error import BizException, ErrorCode
from app.model.biz_response import BizResponse, Error
from app.model.param import find, create
from app.model.param.test_response import TestResponse

app = Flask(__name__)
logger = logging.getLogger(__name__)


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
    req = find.FindOneRequest(**body)
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


if __name__ == '__main__':
    app.run(port=8080, debug=True)
