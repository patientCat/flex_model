from dataclasses import dataclass
from app.model.biz_response import dict_response


@dataclass
@dict_response
class TestResponse:
    name: str
    age: int
