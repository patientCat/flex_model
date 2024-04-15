import json
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, create_engine
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.repo.interface import ProjectRepo, ModelRepo
from app.repo.po import ModelPO, ProjectPO

# 创建基类
Base = declarative_base()

Db_Path = 'sqlite:///database.db'
Engine = create_engine(Db_Path, echo=True)

# 配置日志记录器
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


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


class _ModelPO(Base):
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
        self.engine = Engine
        Base.metadata.create_all(self.engine)

    def get_model_by_name(self, project_id, model_name) -> Optional[ModelPO]:
        Session = sessionmaker(bind=self.engine)
        session = Session()
        model = (session.query(_ModelPO)
                 .filter(and_(_ModelPO.project_id == project_id, _ModelPO.model_name == model_name))
                 .first())
        session.close()
        return model

    def create_model(self, model_ctx: ModelPO) -> None:
        Session = sessionmaker(bind=self.engine)
        session = Session()
        _model_ctx: _ModelPO = _ModelPO()
        copy_value(model_ctx, _model_ctx)
        session.add(_model_ctx)
        session.commit()
        session.close()


class SqlProjectRepo(ProjectRepo):
    def __init__(self):
        super().__init__("sql")
        self.engine = None

    def init(self) -> None:
        self.engine = Engine
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
