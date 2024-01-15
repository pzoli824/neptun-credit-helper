import pytest

from pkg.models.tree import Tree, Node

class TestTree:

    def test_new_tree_initilaization_with_string(self):
        init_value = "for testing"

        t = Tree[str](init_value)

        assert init_value == t.root_node.data

    def test_tree_get_leaf_nodes(self):
        t = Tree[str]("parent")
        child1 = Node("child1")
        child1_child1 = Node("child1_child1")
        child1.append_child_nodes(child1_child1)

        child2 = Node("child2")
        child2_child1 = Node("child2_child1")
        child2_child2 = Node("child2_child2")
        child2.append_child_nodes(child2_child1, child2_child2)
        child2_child2_chil1 = Node("child2_child2_chil1")
        child2_child2.append_child_nodes(child2_child2_chil1)

        expected_leaf_nodes_datas = ["child1_child1", "child2_child1", "child2_child2_chil1"]

        t.append_child_nodes(child1, child2)
        
        assert expected_leaf_nodes_datas == t.get_leaf_nodes_data()
        assert len(t.get_leaf_nodes_data()) is 3

class TestNode:

    def test_new_tree_node_with_parent(self):
        p = Node("parent")
        c = Node("child")
        c2 = Node("child2")

        p.append_child_nodes(c, c2)
        c, c2 = p.children

        assert c.parent is not None
        assert c.parent.data is p.data
        assert p.parent is None
        assert c2.parent is not None
        assert c2.parent.data is p.data

    def test_new_tree_node_without_parent(self):
        n = Node("init")
        data = "node"
        n.data = data

        assert n.parent is None
        assert n.data is data

    def test_append_child_node_to_tree_node(self):
        p = Node("parent")
        c1 = Node("child1")
        c2 = Node("child2")
        assert len(p.children) is 0

        p.append_child_nodes(c1)
        assert len(p.children) is 1

        p.append_child_nodes(c2)
        assert len(p.children) is 2