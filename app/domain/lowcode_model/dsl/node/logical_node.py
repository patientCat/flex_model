from app.domain.lowcode_model.dsl.node.node_base import WhereNode
from typing import List
from abc import abstractmethod


class ContainerNode(WhereNode):
    def __init__(self, node_list: List):
        super().__init__()
        self.node_list = node_list

    @abstractmethod
    def get_logic(self):
        pass

    def to_dict(self):
        if self.node_list is None:
            return None
        val_list = []
        for node in self.node_list:
            if node is not None:
                val_list.append(node.to_dict())
        if len(val_list) == 0:
            return None
        if len(val_list) == 1:
            return val_list[0]
        return {self.get_logic(): val_list}


class AndNode(ContainerNode):
    def __init__(self, node_list):
        super(AndNode, self).__init__(node_list)

    def get_logic(self):
        return "$and"


class OrNode(ContainerNode):
    def __init__(self, node_list):
        super(OrNode, self).__init__(node_list)

    def get_logic(self):
        return "$or"
