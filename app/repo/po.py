import json
from dataclasses import dataclass
from datetime import datetime

"""
定义持久化对象模型
"""


class ProjectPO:
    __tablename__ = 'project'
    id: int
    project_id: str
    connection_info: str
    created_at: datetime
    updated_at: datetime


class ConnectionInfoHolder:
    def __init__(self, connection_info: str):
        self.info_map = json.loads(connection_info)

    def get_db_url(self):
        return self.info_map.get('db_url')


@dataclass
class ModelPO:
    __tablename__ = 'model'
    id: int
    model_name: str
    # namespace 用来逻辑隔离
    namespace: str
    project_id: str
    schema: json
    created_at: datetime
    updated_at: datetime
