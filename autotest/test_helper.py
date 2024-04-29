import requests


class TestHelper:
    @staticmethod
    def check_response(response_data):
        try:
            print(response_data)
            response = response_data["Response"]
            if "Error" in response:
                return False
            else:
                return True
        except Exception as e:
            return False


class ManageClient:
    def __init__(self, *, url, headers):
        self.url = url
        self.headers = headers

    def create_database_instance_t(self, project_id, db_type, db_name, db_url):
        payload = {
            "ProjectId": project_id,
            "Type": db_type,
            "DatabaseName": db_name,
            "DatabaseUrl": db_url,
        }
        response = requests.post(f'{self.url}/CreateDatabaseInstance', json=payload, headers=self.headers)
        response_data = response.json()
        return response_data

    def get_database_instance_t(self, project_id):
        payload = {
            "ProjectId": project_id,
        }
        response = requests.post(f'{self.url}/GetDatabaseInstance', json=payload, headers=self.headers)
        response_data = response.json()
        return response_data

    def delete_database_instance_t(self, project_id):
        payload = {
            "ProjectId": project_id,
        }
        response = requests.post(f'{self.url}/DeleteDatabaseInstance', json=payload, headers=self.headers)
        response_data = response.json()
        return response_data

    def create_model(self, model_name, project_id, schema: dict):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "ModelSchema": schema,
        }
        response = requests.post(f'{self.url}/CreateModel', json=payload, headers=self.headers)
        return response.json()

    def delete_model(self, model_name, project_id):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
        }
        response = requests.post(f'{self.url}/DeleteModel', json=payload, headers=self.headers)
        return response.json()

    def add_column_list(self, model_name, project_id, column_list):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "ColumnList": column_list
        }
        response = requests.post(f'{self.url}/AddColumn', json=payload, headers=self.headers)
        return response.json()

    def delete_column_list(self, model_name, project_id, column_name_list):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
            "ColumnNameList": column_name_list,
        }
        response = requests.post(f'{self.url}/DeleteColumn', json=payload, headers=self.headers)
        return response.json()

    def get_model(self, model_name, project_id):
        payload = {
            "ModelName": model_name,
            "ProjectId": project_id,
        }
        response = requests.post(f'{self.url}/GetModel', json=payload, headers=self.headers)
        response_data = response.json()
        return response_data
