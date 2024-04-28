from typing import Optional, List

from app.repo.po import ModelPO, DatabaseInstancePO

"""
定义操作持久化对象接口
"""


class ModelRepo(object):
    def __init__(self, repo_name) -> None:
        self._repo = repo_name

    def init(self) -> None:
        pass

    def get_model_by_name(self, project_id, model_name) -> Optional[ModelPO]:
        pass

    def get_model_list_page(self, project_id, page_num, page_size) -> List[ModelPO]:
        pass

    def create_model(self, model_ctx: ModelPO) -> None:
        pass

    def delete_model_by_name(self, *, project_id, model_name):
        pass

    def update_schema(self, *, project_id, model_name, schema):
        pass


class DatabaseInstanceRepo(object):
    def __init__(self, repo_name) -> None:
        self._repo = repo_name

    def init(self) -> None:
        pass

    def get_db_instance_by_project_id(self, project_id) -> Optional[DatabaseInstancePO]:
        pass

    def create_db_instance(self, project: DatabaseInstancePO) -> None:
        pass
