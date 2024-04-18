from flask_restful import Resource, reqparse

from app.api.design import DESIGN_SERVICE
from app.common.biz_response import BizResponse
from app.common.param import design


class CreateModel(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ModelName', type=str, required=True)
        parser.add_argument('ModelSchema', type=dict, required=True)
        parser.add_argument('ProjectId', type=str, required=True)
        args = parser.parse_args()

        req = design.CreateModelRequest(**args)
        response = DESIGN_SERVICE.create_model(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class GetModel(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ModelName', type=str, required=True)
        parser.add_argument('ProjectId', type=str, required=True)
        args = parser.parse_args()

        req = design.GetModelRequest(**args)
        response = DESIGN_SERVICE.get_model(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class GetModelList(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('PageSize', type=str, required=False, default=10)
        parser.add_argument('PageNumber', type=str, required=False, default=1)
        parser.add_argument('ProjectId', type=str, required=True)
        args = parser.parse_args()

        req = design.GetModelListRequest(**args)
        response = DESIGN_SERVICE.get_model_list(req)
        success = BizResponse.success(response)
        print(response.dict_msg())
        return success.dict_msg(), 200


class DeleteModel(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ModelName', type=str, required=True)
        parser.add_argument('ProjectId', type=str, required=True)
        args = parser.parse_args()

        req = design.DeleteModelRequest(**args)
        response = DESIGN_SERVICE.delete_model(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200