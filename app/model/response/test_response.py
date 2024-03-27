from dataclasses import dataclass
from ..biz_response import dict_response


@dataclass
@dict_response
class TestResponse:
    name: str
    age: int
