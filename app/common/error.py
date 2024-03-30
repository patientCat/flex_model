from enum import Enum
from typing import Union


class ErrorCode(Enum):
    InternalError = "InternalError"
    InvalidParameter = "InvalidParameter"


class BizException(Exception):
    def __init__(self, code: Union[str, ErrorCode], message: str):
        self.code = code
        self.message = message


class Error:
    def __init__(self, biz_e):
        self.message = biz_e.message
        self.code = biz_e.code

    def to_dict(self):
        return {
            "message": self.message,
            "code": self.code
        }
