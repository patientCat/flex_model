# save this as main.py
import traceback

from flask import Flask, jsonify, request
from flask_restful import Api

from app.common.biz_response import BizResponse, Error
from app.common.bizlogger import LOGGER, init_logger, LogKey
from app.common.error import BizException, ErrorCode
from app.common.thread_local_utils import BIZ_CONTEXT
from app.controller import runtime, manage, common

APP = Flask(__name__)
API = Api(APP)


@APP.before_request
def before_request_func():
    if request.method == "GET":
        LOGGER.info(f"Handling request: {request.method}")
    elif request.method == "POST":
        BIZ_CONTEXT.set_attr(LogKey.action, request.path)
        BIZ_CONTEXT.set_attr(LogKey.request_id, request.headers.get("x-request-id", ""))
        request_body = request.get_json()
        BIZ_CONTEXT.set_attr(LogKey.project_id, request_body.get("ProjectId", ""))
        LOGGER.info(f"Handling request: {request.method} body:{request_body}")


@APP.after_request
def after_request_func(response):
    if request.method == "GET":
        return response
    elif request.method == "POST":
        LOGGER.info(f"Handling response: {response.get_json()}")
        BIZ_CONTEXT.clear()
        return response


init_logger()


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


API.add_resource(runtime.FindOne, '/FindOne')
API.add_resource(runtime.FindMany, '/FindMany')
API.add_resource(runtime.CreateOne, '/CreateOne')
API.add_resource(runtime.CreateMany, '/CreateMany')
API.add_resource(runtime.UpdateOne, '/UpdateOne')
API.add_resource(runtime.UpdateMany, '/UpdateMany')
API.add_resource(runtime.DeleteOne, '/DeleteOne')
API.add_resource(runtime.DeleteMany, '/DeleteMany')

API.add_resource(manage.CreateModel, "/CreateModel")
API.add_resource(manage.DeleteModel, "/DeleteModel")
API.add_resource(manage.GetModel, "/GetModel")
API.add_resource(manage.GetModelList, "/GetModelList")

API.add_resource(common.HealthCheck, "/HealthCheck", "/healthcheck")
API.add_resource(common.TestArgParse, "/TestArgParse", "/testargparse")
if __name__ == '__main__':
    APP.run(port=8080, debug=True)
