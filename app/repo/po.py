import json
from dataclasses import dataclass
from datetime import datetime

from app.common.decorator import readable

"""
定义持久化对象模型
"""


class DatabaseInstancePO:
    __tablename__ = 'database_instance'
    id: int
    project_id: str
    # mongo, mysql
    db_type: str
    host: str
    port: int
    db_name: str
    username: str
    password: str
    created_at: datetime
    updated_at: datetime


class ConnectionInfoHolder:
    def __init__(self, connection_info: str):
        self.info_map = json.loads(connection_info)

    def get_db_url(self):
        return self.info_map.get('db_url')


@readable
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

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.model_name = kwargs.get('model_name')
        self.namespace = kwargs.get('namespace')
        self.project_id = kwargs.get('project_id')
        self.schema = kwargs.get('schema')
        self.created_at: datetime = kwargs.get('created_at')
        self.updated_at: datetime = kwargs.get('updated_at')
