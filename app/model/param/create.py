from dataclasses import dataclass



class CreateOneRequest:
    def __init__(self, **kwargs):
        self.model_name: str = kwargs.get('ModelName')
        self.tenant_id: str = kwargs.get('TenantId')
        self.param: dict = kwargs.get('Param')


@dataclass
class CreateOneResponse:
    id: str

    def dict_msg(self):
        return {
            "Id": self.id,
        }


class CreateManyRequest:
    def __init__(self, **kwargs):
        self.model_name: str = kwargs.get('ModelName')
        self.tenant_id: str = kwargs.get('TenantId')
        self.param: dict = kwargs.get('Param')


@dataclass
class CreateManyResponse:
    id_list: list

    def dict_msg(self):
        return {
            "IdList": self.id_list
        }
