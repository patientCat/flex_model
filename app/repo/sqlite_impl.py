from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.repo.interface import RepoInterface
from app.repo.po import tenant_po


class SqlRepoInterface(RepoInterface):
    def __init__(self):
        super().__init__("sql")
        self.engine = None

    def init(self) -> None:
        self.engine = create_engine('sqlite:///sqlalchemy_example.db')
        tenant_po.Base.metadata.create_all(self.engine)

    def get_tenant_by_tenant_id(self, tenant_id) -> Optional[tenant_po.TenantPO]:
        Session = sessionmaker(bind=self.engine)
        session = Session()
        tenant = session.query(tenant_po.TenantPO).filter(tenant_po.TenantPO.tenant_id == tenant_id).first()
        session.close()
        return tenant

    def create_tenant(self, tenant: tenant_po.TenantPO) -> None:
        Session = sessionmaker(bind=self.engine)
        session = Session()
        session.add(tenant)
        session.commit()
        session.close()
