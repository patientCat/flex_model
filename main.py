# save this as main.py
import traceback

from flask import Flask, jsonify
from flask_restful import Api, Resource
from loguru import logger

from app.common.biz_response import BizResponse, Error
from app.common.error import BizException, ErrorCode
from app.controller import runtime, design

APP = Flask(__name__)
API = Api(APP)



@APP.errorhandler(Exception)
def error_handler(e):
    """
    全局异常捕获
    """
    logger.error("error={}", e)
    logger.error("traceback={}", traceback.format_exc())
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

API.add_resource(design.CreateModel, "/CreateModel")
API.add_resource(design.GetModel, "/GetModel")
API.add_resource(design.GetModelList, "/GetModelList")

if __name__ == '__main__':
    APP.run(port=8080, debug=True)
