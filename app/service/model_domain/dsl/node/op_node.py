from node_base import Node
from abc import abstractmethod


class LeafNode(Node):
    def __init__(self, key, op, val):
        super().__init__()
        self.key = key
        self.op = op
        self.val = val

    @abstractmethod
    def get_op(self) -> str:
        pass

    def to_dict(self):
        return {self.key: {self.get_op(): self.val}}


"""
空节点，用来站位的，不起任何作用
"""


class EmptyNode(LeafNode):
    def __init__(self):
        super().__init__(None, None, None)

    def get_op(self) -> str:
        pass

    def to_dict(self):
        return {}


EMPTY_NODE = EmptyNode()


class EqNode(LeafNode):
    def __init__(self, key, op, val):
        super().__init__(key, op, val)

    def get_op(self):
        return "$eq"


class NeqNode(LeafNode):
    def __init__(self, key, op, val):
        super().__init__(key, op, val)

    def get_op(self):
        return "$ne"


class InNode(LeafNode):
    def __init__(self, key, op, val):
        super().__init__(key, op, val)

    def get_op(self):
        return "$in"


class NotInNode(LeafNode):
    def __init__(self, key, op, val):
        super().__init__(key, op, val)

    def get_op(self):
        return "$nin"
