# save this as main.py
import traceback

from flask import Flask, jsonify
from flask_restful import reqparse, Api, Resource
from loguru import logger

from app.api.runtime import RuntimeService
from app.common.error import BizException, ErrorCode
from app.model.biz_response import BizResponse, Error
from app.model.param import runtime

APP = Flask(__name__)
API = Api(APP)

RUNTIME_SERVICE = RuntimeService.create()

PARSER = reqparse.RequestParser()
PARSER.add_argument('ModelName', type=str, required=True)
PARSER.add_argument('ProjectId', type=str, required=True)
PARSER.add_argument('Param', type=dict, required=True)


class FindOne(Resource):
    def post(self):
        args = PARSER.parse_args()
        req = runtime.FindOneRequest(**args)
        response = RUNTIME_SERVICE.find_one(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class FindMany(Resource):
    def post(self):
        args = PARSER.parse_args()
        req = runtime.FindManyRequest(**args)
        response = RUNTIME_SERVICE.find_many(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class CreateOne(Resource):
    def post(self):
        args = PARSER.parse_args()
        req = runtime.CreateOneRequest(**args)
        response = RUNTIME_SERVICE.create_one(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 201


class CreateMany(Resource):
    def post(self):
        args = PARSER.parse_args()
        logger.info("args={}", args)
        req = runtime.CreateManyRequest(**args)
        response = RUNTIME_SERVICE.create_many(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 201


class UpdateOne(Resource):
    def post(self):
        args = PARSER.parse_args()
        req = runtime.UpdateOneRequest(**args)
        response = RUNTIME_SERVICE.update_one(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 201


class UpdateMany(Resource):
    def post(self):
        args = PARSER.parse_args()
        logger.info("args={}", args)
        req = runtime.UpdateManyRequest(**args)
        response = RUNTIME_SERVICE.update_many(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 201


class DeleteOne(Resource):
    def post(self):
        args = PARSER.parse_args()
        req = runtime.DeleteOneRequest(**args)
        response = RUNTIME_SERVICE.delete_one(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 201


class DeleteMany(Resource):
    def post(self):
        args = PARSER.parse_args()
        logger.info("args={}", args)
        req = runtime.DeleteManyRequest(**args)
        response = RUNTIME_SERVICE.delete_many(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 201


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


API.add_resource(FindOne, '/FindOne')
API.add_resource(FindMany, '/FindMany')
API.add_resource(CreateOne, '/CreateOne')
API.add_resource(CreateMany, '/CreateMany')
API.add_resource(UpdateOne, '/UpdateOne')
API.add_resource(UpdateMany, '/UpdateMany')
API.add_resource(DeleteOne, '/DeleteOne')
API.add_resource(DeleteMany, '/DeleteMany')

if __name__ == '__main__':
    APP.run(port=8080, debug=True)
