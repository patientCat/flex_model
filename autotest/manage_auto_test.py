import json
import unittest

from autotest.test_helper import ManageClient, TestHelper


class TestDatabaseInstance(unittest.TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:8080'
        self.headers = {'Content-Type': 'application/json'}
        self.project_id = "default"
        self.manage_client = ManageClient(url=self.url, headers=self.headers)

    def test_database_instance(self):
        create_response = self.manage_client.create_database_instance_t(self.project_id, "mongo", "my_database",
                                                                        "mongodb://localhost:27017/")
        self.assertTrue(TestHelper.check_response(create_response))

        get_response = self.manage_client.get_database_instance_t(self.project_id)
        self.assertTrue(TestHelper.check_response(get_response))

        delete_response = self.manage_client.delete_database_instance_t(self.project_id)
        self.assertTrue(TestHelper.check_response(delete_response))


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8080'
        self.headers = {'Content-Type': 'application/json'}
        self.manage_client = ManageClient(url=self.url, headers=self.headers)
        self.project_id = "default"
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
        self.manage_client.create_database_instance_t(self.project_id, "mongo", "my_database",
                                                      "mongodb://localhost:27017/")
        self.manage_client.delete_model("user", self.project_id)

    def tearDown(self):
        self.manage_client.delete_database_instance_t(self.project_id)

    def test_create(self):
        self.manage_client.create_model("user", self.project_id, self.user_schema)
        self.manage_client.delete_model("user", self.project_id)

    def test_column(self):
        self.manage_client.create_model("user", self.project_id, self.user_schema)
        self.manage_client.add_column_list("user",
                                           self.project_id,
                                           [
                                               {"name": "delete", "format": "xShortText", "type": "string"},
                                               {"name": "exist", "format": "xShortText", "type": "string"}])
        self.manage_client.delete_column_list("user", self.project_id, ["delete"])
        response = self.manage_client.get_model("user", self.project_id)
        schema = response['Response']['Model']['Schema']
        json_schema = json.loads(schema)
        properties = json_schema['properties']
        self.assertTrue('exist' in properties)
        self.manage_client.delete_model("user", self.project_id)
