"""
thread_local 的工具类
"""
import threading
from typing import Any


class ThreadLocalContext:
    def __init__(self):
        self.__thread_local = threading.local()

    def get_context(self) -> dict:
        value = getattr(self.__thread_local, "value", None)
        if value is None:
            value = {}
        return value

    def get_attr(self, attr: str) -> Any:
        context: dict = self.get_context()
        return context.get(attr, None)

    def get_attr_and_set(self, attr: str, value: Any):
        attr_value = self.get_attr(attr)
        if attr_value is None:
            attr_value = value
            self.set_attr(attr, attr_value)

        return attr_value

    def set_attr(self, attr: str, value) -> None:
        context: dict = self.get_context()
        context[attr] = value
        self.__thread_local.value = context

    def clear(self) -> None:
        self.get_context().clear()


BIZ_CONTEXT: ThreadLocalContext = ThreadLocalContext()
