import unittest
import requests

"""
项目的标准测试
"""


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8080'
        self.headers = {'Content-Type': 'application/json'}


    def test_find_one(self):
        payload = {
            "ModelName": "luke_test",
            "ProjectId": "tnt_test",
            "Param": {
                "select": {
                    "id": 1,
                    "name": 1
                },
                "limit": 10,
                "offset": 0,
                "where": {
                    "name": "foo"
                }
            }
        }
        response = requests.post(f'{self.url}/FindOne', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_find_one_with_count(self):
        payload = {
            "ModelName": "luke_test",
            "ProjectId": "tnt_test",
            "Param": {
                "select": {
                    "id": 1,
                    "name": 1
                },
                "limit": 10,
                "offset": 0,
                "where": {
                    "name": "foo"
                },
                "withCount": True
            }
        }
        response = requests.post(f'{self.url}/FindOne', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_find_many(self):
        payload = {
            "ModelName": "luke_test",
            "ProjectId": "tnt_test",
            "Param": {
                "select": {
                    "id": 1,
                    "name": 1
                },
                "limit": 10,
                "offset": 0,
                "where": {
                    "name": "foo"
                },
                "withCount": True
            }
        }
        response = requests.post(f'{self.url}/FindOne', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_create_one(self):
        payload = {
            "ModelName": "luke_test",
            "ProjectId": "tnt_test",
            "Param": {
                "select": {
                    "id": 1,
                    "name": 1
                },
                "limit": 10,
                "offset": 0,
                "where": {
                    "name": "foo"
                },
                "withCount": True
            }
        }
        response = requests.post(f'{self.url}/FindOne', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_create_many(self):
        payload = {
            "ModelName": "luke_test",
            "ProjectId": "tnt_test",
            "Param": {
                "select": {
                    "id": 1,
                    "name": 1
                },
                "limit": 10,
                "offset": 0,
                "where": {
                    "name": "foo"
                },
                "withCount": True
            }
        }
        response = requests.post(f'{self.url}/FindOne', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_update_one(self):
        payload = {
            "ModelName": "luke_test",
            "ProjectId": "tnt_test",
            "Param": {
                "select": {
                    "id": 1,
                    "name": 1
                },
                "limit": 10,
                "offset": 0,
                "where": {
                    "name": "foo"
                },
                "withCount": True
            }
        }
        response = requests.post(f'{self.url}/FindOne', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_update_many(self):
        payload = {
            "ModelName": "luke_test",
            "ProjectId": "tnt_test",
            "Param": {
                "select": {
                    "id": 1,
                    "name": 1
                },
                "limit": 10,
                "offset": 0,
                "where": {
                    "name": "foo"
                },
                "withCount": True
            }
        }
        response = requests.post(f'{self.url}/FindOne', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_one(self):
        payload = {
            "ModelName": "luke_test",
            "ProjectId": "tnt_test",
            "Param": {
                "select": {
                    "id": 1,
                    "name": 1
                },
                "limit": 10,
                "offset": 0,
                "where": {
                    "name": "foo"
                },
                "withCount": True
            }
        }
        response = requests.post(f'{self.url}/FindOne', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_many(self):
        payload = {
            "ModelName": "luke_test",
            "ProjectId": "tnt_test",
            "Param": {
                "select": {
                    "id": 1,
                    "name": 1
                },
                "limit": 10,
                "offset": 0,
                "where": {
                    "name": "foo"
                },
                "withCount": True
            }
        }
        response = requests.post(f'{self.url}/FindOne', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
