# save this as main.py
import traceback

from flask import Flask, jsonify, request
from loguru import logger

from app.api.context import TestContextHolder
from app.api.runtime import RuntimeService
from app.common.error import BizException, ErrorCode
from app.model.biz_response import BizResponse, Error
from app.model.param import find, create
from app.model.param.test_response import TestResponse

app = Flask(__name__)




@app.route("/")
def hello():
    res = TestResponse("luke", 12)
    print(res)
    success = BizResponse.success(res)
    return jsonify(success.dict_msg()), success.status, success.header


context_holder = TestContextHolder()
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
    logger.info('body={}'.format(str(body)))
    req = create.CreateOneRequest(**body)
    response = runtime_service.createOne(req)
    logger.info('response={}'.format(str(response)))
    success = BizResponse.success(response)
    return jsonify(success.dict_msg()), success.status, success.header


@app.errorhandler(Exception)
def error_handler(e):
    """
    全局异常捕获
    """
    logger.error("error={}", e)
    logger.error("traceback={}", traceback.format_exc())
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
