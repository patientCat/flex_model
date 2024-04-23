import functools

from flask_restful import reqparse, Resource

from app.service.runtime import RUNTIME_SERVICE
from app.common.biz_response import BizResponse
from app.common.param import runtime

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
        req = runtime.DeleteManyRequest(**args)
        response = RUNTIME_SERVICE.delete_many(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 201