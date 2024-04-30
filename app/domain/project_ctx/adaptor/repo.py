from typing import Optional

from app.domain.lowcode_model.dsl.dml_domain import FindDomain, FindManyDomain, CreateDomain, CreateManyDomain, \
    UpdateDomain, UpdateManyDomain, DeleteDomain, DeleteManyDomain
from app.domain.lowcode_model.dsl.dsl_domain import CreateTableDomain


class RepoService:
    def apply_find(self, find_domain: FindDomain) -> (Optional[dict], Optional[int]):
        raise NotImplementedError

    def apply_find_many(self, find_many_domain: FindManyDomain) -> (Optional[list], Optional[int]):
        raise NotImplementedError

    def apply_create(self, create_domain: CreateDomain) -> str:
        raise NotImplementedError

    def apply_create_many(self, create_domain: CreateManyDomain) -> list:
        raise NotImplementedError

    def apply_update(self, update_domain: UpdateDomain) -> int:
        raise NotImplementedError

    def apply_update_many(self, update_domain: UpdateManyDomain) -> int:
        raise NotImplementedError

    def apply_delete(self, delete_domain: DeleteDomain) -> int:
        raise NotImplementedError

    def apply_delete_many(self, domain: DeleteManyDomain):
        raise NotImplementedError

    def create_table(self, domain: CreateTableDomain):
        raise NotImplementedError
