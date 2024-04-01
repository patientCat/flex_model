from dataclasses import dataclass

from app.model.biz_response import dict_response


class CreateOneRequest:
    def __init__(self, **kwargs):
        self.model_name: str  = kwargs.get('model_name')
        self.model_namespace: str = kwargs.get('model_namespace')
        self.tenant_id: str = kwargs.get('tenant_id')
        self.param: dict = kwargs.get('param')


@dataclass
@dict_response
class CreateOneResponse:
    id: str
