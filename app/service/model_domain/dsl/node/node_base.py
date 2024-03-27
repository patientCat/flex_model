from abc import abstractmethod, ABCMeta

"""
节点校验类
"""


class Node(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass




