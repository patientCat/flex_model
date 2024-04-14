import copy
import json
from datetime import datetime
from typing import Optional

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

from app.repo.interface import ProjectRepo, ModelRepo

from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

from app.repo.po import ModelContextPO, ProjectPO

# 创建基类
Base = declarative_base()


def copy_value(from_cls, to_cls):
    for k, v in from_cls.__dict__.items():
        setattr(to_cls, k, v)


class _ProjectPO(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    project_id = Column(String)
    connection_info = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



class ConnectionInfoHolder:
    def __init__(self, connection_info: str):
        self.info_map = json.loads(connection_info)

    def get_db_url(self):
        return self.info_map.get('db_url')


class _ModelContextPO(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    # namespace 用来逻辑隔离
    namespace = Column(String, default="default")
    project_id = Column(String)
    schema = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('project_id', 'model_name', name='unique_project_id_name'),
    )


class SqlModelRepo(ModelRepo):
    def __init__(self):
        super().__init__("sql")
        self.engine = None

    def init(self) -> None:
        self.engine = create_engine('sqlite:///sqlalchemy_example.db')
        Base.metadata.create_all(self.engine)

    def get_model_by_name(self, project_id, model_name) -> Optional[ModelContextPO]:
        Session = sessionmaker(bind=self.engine)
        session = Session()
        model = (session.query(_ModelContextPO)
                 .filter(and_(_ModelContextPO.project_id == project_id, _ModelContextPO.model_name == model_name))
                 .first())
        session.close()
        return model

    def create_model(self, model_ctx: ModelContextPO) -> None:
        Session = sessionmaker(bind=self.engine)
        session = Session()
        _model_ctx: _ModelContextPO = _ModelContextPO()
        copy_value(model_ctx, _model_ctx)
        session.add(_model_ctx)
        session.commit()
        session.close()


class SqlProjectRepo(ProjectRepo):
    def __init__(self):
        super().__init__("sql")
        self.engine = None

    def init(self) -> None:
        self.engine = create_engine('sqlite:///sqlalchemy_example.db')
        Base.metadata.create_all(self.engine)

    def get_project_by_project_id(self, project_id) -> Optional[ProjectPO]:
        Session = sessionmaker(bind=self.engine)
        session = Session()
        project = (session.query(_ProjectPO)
                    .filter(_ProjectPO.project_id == project_id)
                    .first())
        session.close()

        return project

    def create_project(self, project: ProjectPO) -> None:
        Session = sessionmaker(bind=self.engine)
        session = Session()
        _project = _ProjectPO()
        copy_value(project, _project)
        session.add(_project)
        session.commit()
        session.close()
