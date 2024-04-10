# save this as main.py
import traceback

from flask import Flask, jsonify
from flask_restful import reqparse, Api, Resource
from loguru import logger

from app.api.context import TestContextHolder
from app.api.runtime import RuntimeService
from app.common.error import BizException, ErrorCode
from app.model.biz_response import BizResponse, Error
from app.model.param import runtime
from app.model.param.test_response import TestResponse

app = Flask(__name__)
api = Api(app)


@app.route("/")
def hello():
    res = TestResponse("luke", 12)
    print(res)
    success = BizResponse.success(res)
    return jsonify(success.dict_msg()), success.status, success.header


context_holder = TestContextHolder()
runtime_service = RuntimeService(context=context_holder)

parser = reqparse.RequestParser()
parser.add_argument('ModelName', type=str, required=True)
parser.add_argument('TenantId', type=str, required=True)
parser.add_argument('Param', type=dict, required=True)


class FindOne(Resource):
    def post(self):
        args = parser.parse_args()
        req = runtime.FindOneRequest(**args)
        response = runtime_service.findOne(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class FindMany(Resource):
    def post(self):
        args = parser.parse_args()
        req = runtime.FindOneRequest(**args)
        response = runtime_service.findMany(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class CreateOne(Resource):
    def post(self):
        args = parser.parse_args()
        req = runtime.CreateOneRequest(**args)
        response = runtime_service.createOne(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 201


class CreateMany(Resource):
    def post(self):
        args = parser.parse_args()
        logger.info("args={}", args)
        req = runtime.CreateManyRequest(**args)
        response = runtime_service.createMany(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 201


class UpdateOne(Resource):
    def post(self):
        args = parser.parse_args()
        req = runtime.CreateOneRequest(**args)
        response = runtime_service.updateOne(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 201


class UpdateMany(Resource):
    def post(self):
        args = parser.parse_args()
        logger.info("args={}", args)
        req = runtime.CreateManyRequest(**args)
        response = runtime_service.updateMany(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 201


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


api.add_resource(FindOne, '/FindOne')
api.add_resource(FindMany, '/FindMany')
api.add_resource(CreateOne, '/CreateOne')
api.add_resource(CreateMany, '/CreateMany')
api.add_resource(UpdateOne, '/UpdateOne')
api.add_resource(UpdateMany, '/UpdateMany')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
