from enum import Enum


class ErrorCode(Enum):
    InternalError = "InternalError"
    InvalidParameter = "InvalidParameter"


class BizException(Exception):
    def __init__(self, code: ErrorCode, message: str):
        self.code = code
        self.message = message


class Error:
    def __init__(self, msg: str, code: str):
        self.message = msg
        self.code = code

    def dict_msg(self):
        return {
            "Error": {
                "Message": self.message,
                "Code": self.code
            }
        }
