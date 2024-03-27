# save this as app.py
from flask import Flask, jsonify
from model.biz_response import BizResponse
from model.response.test_response import TestResponse
from common.error import BizException, Error
from common.errorcode import *

app = Flask(__name__)


@app.route("/")
def hello():
    res = TestResponse("luke", 12)
    print(res)
    success = BizResponse.success(res)
    return jsonify(success.dict_msg()), success.status, success.header


@app.route("/findOne")
def findOne():
    return "findOne"


@app.route("/findMany")
def findMany():
    return "findMany"


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
