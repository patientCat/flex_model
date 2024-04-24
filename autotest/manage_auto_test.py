import json
import unittest

import requests


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8080'
        self.headers = {'Content-Type': 'application/json'}
        self.user_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "id": {
                    "name": "id",
                    "type": "string",
                    "format": "xShortText"
                },
                "name": {
                    "name": "name",
                    "type": "string",
                    "format": "xShortText"
                },
                "age": {
                    "name": "age",
                    "type": "number",
                    "format": "xNumber"
                },
                "email": {
                    "name": "email",
                    "type": "string",
                    "format": "email"
                },
                "profileList": {
                    "name": "profileList",
                    "type": "object",
                    "properties": {

                    },
                    "format": "xOneToMany",
                    "xRelation": {
                        "field": "id",
                        "relatedField": "userId",
                        "relatedModelName": "profile"
                    }
                }
            },
            "required": [
                "name",
                "age"
            ]
        }
        self.delete_model("user", "default")

    def test_create(self):
        self.create_model("user", "default", self.user_schema)
        self.delete_model("user", "default")

    def test_column(self):
        self.create_model("user", "default", self.user_schema)
        self.add_column_list("user",
                             "default",
                             [
                                 {"name": "delete", "format": "xShortText", "type": "string"},
                                 {"name": "exist", "format": "xShortText", "type": "string"}])
        self.delete_column_list("user", "default", ["delete"])
        response = self.get_model("user", "default")
        schema = response['Response']['Model']['Schema']
        json_schema = json.loads(schema)
        properties = json_schema['properties']
        self.assertTrue('exist' in properties)
        self.delete_model("user", "default")

    def create_model(self, model_name, project_id, schema: dict):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "ModelSchema": schema,
        }
        response = requests.post(f'{self.url}/CreateModel', json=payload, headers=self.headers)
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def delete_model(self, model_name, project_id):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
        }
        response = requests.post(f'{self.url}/DeleteModel', json=payload, headers=self.headers)
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def add_column_list(self, model_name, project_id, column_list):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "ColumnList": column_list
        }
        response = requests.post(f'{self.url}/AddColumn', json=payload, headers=self.headers)
        print(response.json())

    def delete_column_list(self, model_name, project_id, column_name_list):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "ColumnNameList": column_name_list,
        }
        response = requests.post(f'{self.url}/DeleteColumn', json=payload, headers=self.headers)
        print(response.json())

    def get_model(self, model_name, project_id):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
        }
        response = requests.post(f'{self.url}/GetModel', json=payload, headers=self.headers)
        print(response.json())
        response_data = response.json()
        return response_data
