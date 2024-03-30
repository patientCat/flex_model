import json

from app.service.model_domain.dsl.node import node_base, op_node, logical_node
from app.common.error import BizException
from app.common import errorcode
from typing import Dict, Optional


def get_first_pair(query: Dict):
    if query is None:
        return None
    for key, val in query.items():
        return key, val


class NodeFactory:
    KEY_WHERE = "where"

    def __init__(self, strict: bool = True, ignore_invalid_op: bool = False):
        self.strict = strict
        self.ignore_invalid_op = ignore_invalid_op
        pass

    def create_node(self, dict_param: Optional[dict]) -> node_base.WhereNode:
        if dict_param is None or self.KEY_WHERE not in dict_param:
            return op_node.EMPTY_NODE
        else:
            return self._create_node_from_dict(dict_param[self.KEY_WHERE])

    def _create_node(self, query: str) -> node_base.WhereNode:
        if query is None or query == "":
            return op_node.EMPTY_NODE
        json_query = json.loads(query)
        return self._create_node_from_dict(json_query)

    def _create_node_from_dict(self, query: Dict) -> node_base.WhereNode:
        if query is None:
            return op_node.EMPTY_NODE
        pair = get_first_pair(query)
        if pair is None:
            return op_node.EMPTY_NODE
        key, obj = pair
        if key.startswith("$"):
            return self._process_logical_node(key, obj)
        else:
            node_list = self._process_and_op_list(query)
            return logical_node.AndNode(node_list)

    def _process_and_op_list(self, query: Dict):
        node_list = []
        for key, obj in query.items():
            node_ = self._create_op_node(key, obj)
            if node_ is not None:
                node_list.append(node_)
            continue
        return node_list

    def _create_op_node(self, key: str, obj: Dict) -> Optional[node_base.WhereNode]:
        if not isinstance(obj, dict):
            if isinstance(obj, list):
                raise BizException(errorcode.ErrorCode_InvalidParameter,
                                   f"invalid type {obj}, type={type(obj)} is not dict or single_val")
            else:
                return op_node.EqNode(key, "$eq", obj)
        op, val = get_first_pair(obj)
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
        if op == "$gt":
            return op_node.GtNode(key, op, val)
        if op == "$gte":
            return op_node.GteNode(key, op, val)
        if op == "$lt":
            return op_node.LtNode(key, op, val)
        if op == "$lte":
            return op_node.LteNode(key, op, val)

        if self.ignore_invalid_op:
            return None
        else:
            raise BizException(errorcode.ErrorCode_InvalidParameter, f"op={op} is invalid")

    def _process_logical_node(self, logical_key, obj):
        if not isinstance(obj, list):
            raise BizException(errorcode.ErrorCode_InvalidParameter,
                               f"logical node expect list type but get {type(obj)}")

        node_list = []
        for query in obj:
            node = self._create_node_from_dict(query)
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
