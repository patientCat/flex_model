import sqlalchemy
from flask_restful import Resource, reqparse

from app.common.error import BizException, ErrorCode
from app.service.manage import MANAGE_SERVICE
from app.common.biz_response import BizResponse
from app.common.param import manage


class CreateModel(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ModelName', type=str, required=True)
        parser.add_argument('ModelSchema', type=dict, required=True)
        parser.add_argument('ProjectId', type=str, required=True)
        args = parser.parse_args()

        req = manage.CreateModelRequest(**args)
        response = MANAGE_SERVICE.create_model(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class GetModel(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ModelName', type=str, required=True)
        parser.add_argument('ProjectId', type=str, required=True)
        args = parser.parse_args()

        req = manage.GetModelRequest(**args)
        response = MANAGE_SERVICE.get_model(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class GetModelList(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('PageSize', type=str, required=False, default=10)
        parser.add_argument('PageNumber', type=str, required=False, default=1)
        parser.add_argument('ProjectId', type=str, required=True)
        args = parser.parse_args()

        req = manage.GetModelListRequest(**args)
        response = MANAGE_SERVICE.get_model_list(req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class DeleteModel(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ModelName', type=str, required=True)
        parser.add_argument('ProjectId', type=str, required=True)
        args = parser.parse_args()

        req = manage.DeleteModelRequest(**args)
        response = MANAGE_SERVICE.delete_model(req=req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class AddColumn(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ModelName', type=str, required=True)
        parser.add_argument('ProjectId', type=str, required=True)
        parser.add_argument('ColumnList', type=dict, action="append", required=True)
        args = parser.parse_args()
        print(f"args={args}")

        req = manage.AddColumnRequest(**args)
        response = MANAGE_SERVICE.add_column(req=req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class DeleteColumn(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ModelName', type=str, required=True)
        parser.add_argument('ProjectId', type=str, required=True)
        parser.add_argument('ColumnNameList', type=str, action="append", required=True)
        args = parser.parse_args()

        req = manage.DeleteColumnRequest(**args)
        response = MANAGE_SERVICE.delete_column(req=req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class CreateDatabaseInstance(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ProjectId', type=str, required=True)
        parser.add_argument('Type', type=str, choices=["mongo", "mysql"], required=True)
        parser.add_argument('Host', type=str, required=True)
        parser.add_argument('DatabaseName', type=str, required=True)
        parser.add_argument('Username', type=str, required=True)
        parser.add_argument('Port', type=int, required=True)
        parser.add_argument('Password', type=str, required=True)
        args = parser.parse_args()

        req = manage.CreateDatabaseInstanceRequest(**args)
        response = MANAGE_SERVICE.create_database_instance(req=req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class DeleteDatabaseInstance(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ProjectId', type=str, required=True)
        args = parser.parse_args()

        req = manage.DeleteDatabaseInstanceRequest(**args)
        response = MANAGE_SERVICE.delete_database_instance(req=req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200


class TestDatabaseInstance(Resource):
    pass


class GetDatabaseInstance(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ProjectId', type=str, required=True)
        args = parser.parse_args()

        req = manage.GetDatabaseInstanceRequest(**args)
        response = MANAGE_SERVICE.get_database_instance(req=req)
        success = BizResponse.success(response)
        return success.dict_msg(), 200