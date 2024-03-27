import json

import node_base
from app.common.error import BizException
from app.common import errorcode
from typing import Dict, Optional
import op_node
import logical_node


class NodeFactory:
    def __init__(self, strict: bool = True, ignore_invalid_op: bool = False):
        self.strict = strict
        self.ignore_invalid_op = ignore_invalid_op
        pass

    def create_node(self, query: str) -> node_base.Node:
        if query is None or query == "":
            return op_node.EMPTY_NODE
        json_query = json.loads(query)
        return self.create_node_from_dict(json_query)

    def create_node_from_dict(self, query: Dict) -> node_base.Node:
        if query is None:
            return op_node.EMPTY_NODE
        pair = self.get_first_pair(query)
        if pair is None:
            return op_node.EMPTY_NODE
        key, obj = pair
        if key.startswith("$"):
            return self.process_logical_node(key, obj)
        else:
            node_list = self.process_and_op_list(query)
            return logical_node.AndNode(node_list)

    def process_and_op_list(self, query: Dict):
        node_list = []
        for key, obj in query.items():
            node_ = self.create_op_node(key, obj)
            if node_ is not None:
                node_list.append(node_)
            continue
        return node_list

    def create_op_node(self, key: str, obj: Dict) -> Optional[node_base.Node]:
        if not isinstance(obj, dict):
            if isinstance(obj, list):
                raise BizException(errorcode.ErrorCode_InvalidParameter,
                                   f"invalid type {obj}, type={type(obj)} is not dict or single_val")
            else:
                return op_node.EqNode(key, "$eq", obj)
        op, val = self.get_first_pair(obj)
        if self.ignore_invalid_op and not op.startswith("$"):
            return None
        if op == "$eq":
            return op_node.EqNode(key, op, val)
        if op == "$ne" or op == "$neq":
            return op_node.NeqNode(key, op, val)
        if op == "$in":
            return op_node.InNode(key, op, val)
        if op == "$nin":
            return op_node.NotInNode(key, op, val)

        if self.ignore_invalid_op:
            return None
        else:
            raise BizException(errorcode.ErrorCode_InvalidParameter, f"op={op} is invalid")

    def get_first_pair(self, query: Dict):
        if query is None:
            return None
        for key, val in query.items():
            return key, val

    def process_logical_node(self, logical_key, obj):
        if not isinstance(obj, list):
            raise BizException(errorcode.ErrorCode_InvalidParameter,
                               f"logical node expect list type but get {type(obj)}")

        node_list = []
        for query in obj:
            node = self.create_node_from_dict(query)
            if node is not None:
                node_list.append(node)
        if len(node_list) == 0:
            return None

        if logical_key == "$and":
            return logical_node.AndNode(node_list)
        if logical_key == "$or":
            return logical_node.OrNode(node_list)

        if self.ignore_invalid_op:
            return None
        raise BizException(errorcode.ErrorCode_InvalidParameter, f"invalid logical node = {logical_key}")
