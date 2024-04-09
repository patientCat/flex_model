from typing import Optional

from app.repo.po.tenant_po import TenantPO


class RepoInterface(object):
    def __init__(self, repo_name) -> None:
        self._repo = repo_name

    def init(self) -> None:
        pass

    def get_tenant_by_tenant_id(self, tenant_id) -> Optional[TenantPO]:
        pass

    def create_tenant(self, tenantPo: TenantPO) -> None:
        pass
