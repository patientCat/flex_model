from dataclasses import dataclass

from app.model.biz_response import dict_response


class CreateOneRequest:
    def __init__(self, **kwargs):
        self.model_name: str = kwargs.get('ModelName')
        self.model_namespace: str = kwargs.get('ModelNamespace')
        self.tenant_id: str = kwargs.get('TenantId')
        self.param: dict = kwargs.get('Param')


@dataclass
@dict_response
class CreateOneResponse:
    id: str
