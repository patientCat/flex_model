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
        create_response = self.manage_client.create_database_instance_t(self.project_id, "adaptor", "my_database",
                                                                        "localhost", 27017, "admin", "123456")
        self.assertTrue(TestHelper.check_response(create_response))

        get_response = self.manage_client.get_database_instance_t(self.project_id)
        self.assertTrue(TestHelper.check_response(get_response))

        delete_response = self.manage_client.delete_database_instance_t(self.project_id)
        self.assertTrue(TestHelper.check_response(delete_response))


class TestMongoModel(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8080'
        self.headers = {'Content-Type': 'application/json'}
        self.manage_client = ManageClient(url=self.url, headers=self.headers)
        self.mongo_project = "adaptor"
        self.mysql_project = "mysql"
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
        mongo_resp = self.manage_client.create_database_instance_t(self.mongo_project, "mongo", "my_database",
                                                      "localhost", 27017, "admin", "123456")
        print(mongo_resp)
        mysql_resp = self.manage_client.create_database_instance_t(self.mysql_project, "mysql", "my_database", "localhost",
                                                      3306, "root", "123456")
        print(mysql_resp)
        self.manage_client.delete_model("user", self.mongo_project)

    def tearDown(self):
        self.manage_client.delete_database_instance_t(self.mongo_project)
        self.manage_client.delete_database_instance_t(self.mysql_project)

    def test_create(self):
        create_resp = self.manage_client.create_model("user", self.mongo_project, self.user_schema)
        print(create_resp)

        response = self.manage_client.get_model("user", self.mongo_project)
        print(response)

        delete_resp = self.manage_client.delete_model("user", self.mongo_project)
        print(delete_resp)

    def test_column(self):
        self.manage_client.create_model("user", self.mongo_project, self.user_schema)
        self.manage_client.add_column_list("user",
                                           self.mongo_project,
                                           [
                                               {"name": "delete", "format": "xShortText", "type": "string"},
                                               {"name": "exist", "format": "xShortText", "type": "string"}])
        self.manage_client.delete_column_list("user", self.mongo_project, ["delete"])
        response = self.manage_client.get_model("user", self.mongo_project)
        schema = response['Response']['Model']['Schema']
        json_schema = json.loads(schema)
        properties = json_schema['properties']
        self.assertTrue('exist' in properties)
        self.manage_client.delete_model("user", self.mongo_project)
