import unittest
from factory import NodeFactory
import op_node


class TestFactory(unittest.TestCase):
    def test_basic(self):
        val = []
        val.append({"a": "b"})

    def test_factory(self):
        node_factory = NodeFactory()
        node = node_factory.create_node("{\"a\":1}")
        print(node.to_dict())

    def test_factory_create_cmd_node(self):
        node_factory = NodeFactory()
        # EqNode
        node = node_factory.create_op_node("key", {"$eq": "name"})
        self.assertTrue(isinstance(node, op_node.EqNode))
        # NeqNode
        node = node_factory.create_op_node("key", {"$neq": "name"})
        self.assertTrue(isinstance(node, op_node.NeqNode))
        # InNode
        node = node_factory.create_op_node("key", {"$in": "name"})
        self.assertTrue(isinstance(node, op_node.InNode))
        # NotInNode
        node = node_factory.create_op_node("key", {"$nin": "name"})
        self.assertTrue(isinstance(node, op_node.NotInNode))
