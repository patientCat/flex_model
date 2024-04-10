import re
from enum import Enum
from typing import Optional


class ErrorCode(Enum):
    InternalError = "InternalError"
    InvalidParameter = "InvalidParameter"


## ErrorCode 的Easy版本
class EzErrorCode:
    def __init__(self, error_code: str, error_template: str):
        self.error_code = error_code
        self.error_template = error_template


class EzErrorCodeEnum(Enum):
    InvalidKeyNotFound = EzErrorCode("InvalidParameter", "key {0} not found, please refer to {1}")
    InvalidTypeOfValue = EzErrorCode("InvalidParameter",
                                     "key {0} value type error, type should be {1}, please refer to {2}")


def replace_placeholders(template, *args):
    return template.format(*args)


class BizException(Exception):
    def __init__(self, code: ErrorCode = None, message: str = None, ezcode: EzErrorCodeEnum = None,
                 arg_list: list = None):
        self.__code = None
        if code is not None:
            self.__code = code.value
        self.__ezcode = None
        if ezcode is not None:
            self.__ezcode: Optional[EzErrorCode] = ezcode.value
        self.__arg_list = arg_list
        self.__message = message

    @property
    def code(self):
        if self.__ezcode is None:
            return self.__code
        else:
            return self.__ezcode.error_code

    @property
    def message(self):
        if self.__ezcode is None:
            return self.__message
        else:
            return replace_placeholders(self.__ezcode.error_template, *self.__arg_list)


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
