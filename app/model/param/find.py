from dataclasses import dataclass

from app.model.biz_response import dict_response


@dataclass
class FindOneRequest:
    model_name: str
    param: dict


@dataclass
@dict_response
class FindOneResponse:
    record: dict
    total: int
