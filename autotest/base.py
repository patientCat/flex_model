import unittest
import requests

"""
项目的标准测试
"""


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8080'
        self.headers = {'Content-Type': 'application/json'}
        user_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "format": "xShortText"
                },
                "name": {
                    "type": "string",
                    "format": "xShortText"
                },
                "age": {
                    "type": "number",
                    "format": "xNumber"
                },
                "email": {
                    "type": "string",
                    "format": "email"
                },
                "profileList": {
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

        profile_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "format": "xShortText"
                },
                "biography": {
                    "type": "string",
                    "format": "xShortText"
                },
                "userId": {
                    "type": "string",
                    "format": "xShortText"
                },
                "user": {
                    "type": "object",
                    "properties": {

                    },
                    "format": "xManyToOne",
                    "xRelation": {
                        "field": "userId",
                        "relatedField": "id",
                        "relatedModelName": "user"
                    }
                }
            },
            "required": [
                "biography"
            ]
        }

        self.create_model("user", "default", user_schema)
        self.create_model("profile", "default", profile_schema)

    def tearDown(self):
        self.delete_model("user", "default")
        self.delete_model("profile", "default")

    def create_model(self, model_name, project_id, schema: dict):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "ModelSchema": schema,
        }
        response = requests.post(f'{self.url}/CreateModel', json=payload, headers=self.headers)

    def delete_model(self, model_name, project_id):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
        }
        response = requests.post(f'{self.url}/DeleteModel', json=payload, headers=self.headers)

    """
    case1 : 测试基础的crud
    """

    def test_base_crud(self):
        user_model_name = "user"
        project_id = "default"
        self.clear_table(model_name=user_model_name, project_id=project_id)

        print("step1: create")
        insert_id = self.create_one(model_name=user_model_name, project_id=project_id, data={"name": "luke", "age": 20})
        print(f"step1: create success, insert_id: {insert_id}")

        print("step2: update")
        new_age = 30
        count = self.update_one(model_name=user_model_name, project_id=project_id, where={"id": {"$eq": insert_id}},
                                data={"age": new_age})
        print(f"step2: update success, count: {count}")
        self.assertEqual(count, 1)

        print("step3: find")
        record = self.find_one(model_name=user_model_name, project_id=project_id, where={"id": {"$eq": insert_id}})
        print(f"step3: find success, record: {record}")
        self.assertTrue(record is not None)

        print("step4: delete")
        count = self.delete_one(model_name=user_model_name, project_id=project_id, where={"age": {"$eq": new_age}})
        print(f"step4: delete success, count: {count}")
        self.assertEqual(count, 1)

    """
    case2 : 测试批量crud
    """

    def test_batch_crud(self):
        user_model_name = "user"
        project_id = "default"
        self.clear_table(model_name=user_model_name, project_id=project_id)

        print("step1: create_many")
        insert_id = self.create_many(model_name=user_model_name, project_id=project_id,
                                     data=[{"name": "luke", "age": 20}, {"name": "james", "age": 30}])
        print(f"step1: create_many success, insert_id: {insert_id}")

        print("step2: update")
        new_age = 50
        count = self.update_many(model_name=user_model_name, project_id=project_id, where={"id": {"$in": insert_id}},
                                 data={"age": new_age})
        print(f"step2: update success, count: {count}")
        self.assertEqual(count, 2)

        print("step3: find")
        record = self.find_many(model_name=user_model_name, project_id=project_id, where={"id": {"$in": insert_id}})
        print(f"step3: find success, record: {record}")
        self.assertTrue(record is not None)

        print("step4: delete")
        count = self.delete_many(model_name=user_model_name, project_id=project_id, where={"age": {"$eq": new_age}})
        print(f"step4: delete success, count: {count}")
        self.assertEqual(count, 2)

    """
    case3 : 测试关联关系查询
    """

    def test_query_relation(self):
        # 测试关联查询
        user_model_name = "user"
        profile_model_name = "profile"
        project_id = "default"
        self.clear_table(model_name=user_model_name, project_id=project_id)

        print("begin: create user")
        user_insert_id = self.create_one(model_name=user_model_name, project_id=project_id,
                                         data={"name": "luke", "age": 20})
        print(f"end: create success, insert_id: {user_insert_id}")

        print("begin: create profile and relate user")
        profile_insert_id_list = self.create_many(
            model_name=profile_model_name,
            project_id=project_id,
            data=[
                {"biography": "this is luke, a python coder", "userId": user_insert_id},
                {"biography": "this is james, a cpp coder", "userId": user_insert_id}
            ]
        )
        print(f"end: create success, insert_id: {profile_insert_id_list}")

        print("begin: find and many2one relation")

        record = self.find_one(model_name=profile_model_name, project_id=project_id,
                               where={"id": {"$eq": profile_insert_id_list[0]}}, include={"user": True})
        print(f"end: find success, record: {record}")
        self.assertTrue(record is not None)
        self.assertTrue('user' in record)

        print("begin: findMany and relation")
        record = self.find_many(model_name=profile_model_name, project_id=project_id,
                                where={"id": {"$eq": profile_insert_id_list[0]}}, include={"user": True})
        print(f"end: find success, record: {record}")
        self.assertTrue(record is not None)
        self.assertTrue('user' in record[0])

        print("begin: find and one2many relation")

        record = self.find_one(model_name=user_model_name, project_id=project_id,
                               where={"id": {"$eq": user_insert_id}}, include={"profileList": True})
        print(f"end: find success, record: {record}")
        self.assertTrue(record is not None)
        self.assertTrue('profileList' in record)

        print(f"begin: delete user with {user_insert_id}")
        count = self.delete_one(model_name=user_model_name, project_id=project_id,
                                where={"id": {"$eq": user_insert_id}})
        print(f"end: delete success, count: {count}")
        self.assertEqual(count, 1)

        print(f"begin: delete profile with {profile_insert_id_list}")
        count = self.delete_many(model_name=profile_model_name, project_id=project_id,
                                 where={"id": {"$in": profile_insert_id_list}})
        print(f"end: delete success, count: {count}")
        self.assertEqual(count, 2)

    def create_one(self, *, model_name, project_id, data: dict) -> str:
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "Param": {
                "data": data
            }
        }
        response = requests.post(f'{self.url}/CreateOne', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        return response.json().get("Response").get("Id")

    def update_one(self, *, model_name, project_id, where: dict, data: dict):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "Param": {
                "where": where,
                "data": data
            }
        }
        response = requests.post(f'{self.url}/UpdateOne', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        return response.json().get("Response").get("Count")

    def find_one(self, *, model_name, project_id, where: dict, include: dict = None):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "Param": {
                "where": where,
                "include": include,
            }
        }
        response = requests.post(f'{self.url}/FindOne', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        return response.json().get("Response").get("Record")

    def delete_one(self, *, model_name, project_id, where: dict):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "Param": {
                "where": where,
            }
        }
        response = requests.post(f'{self.url}/DeleteOne', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        return response.json().get("Response").get("Count")

    def create_many(self, model_name, project_id, data) -> list:
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "Param": {
                "data": data
            }
        }
        response = requests.post(f'{self.url}/CreateMany', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        return response.json().get("Response").get("IdList")

    def update_many(self, model_name, project_id, where, data):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "Param": {
                "where": where,
                "data": data
            }
        }
        response = requests.post(f'{self.url}/UpdateMany', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        return response.json().get("Response").get("Count")

    def find_many(self, *, model_name, project_id, where, include: dict = None):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "Param": {
                "where": where,
                "include": include,
            }
        }
        response = requests.post(f'{self.url}/FindMany', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        return response.json().get("Response").get("Record")

    def delete_many(self, model_name, project_id, where):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "Param": {
                "where": where,
            }
        }
        response = requests.post(f'{self.url}/DeleteMany', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        return response.json().get("Response").get("Count")

    def clear_table(self, model_name, project_id):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "Param": {
                "where": {}
            }
        }
        response = requests.post(f'{self.url}/DeleteMany', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        return response.json().get("Response").get("Count")


if __name__ == '__main__':
    unittest.main()
